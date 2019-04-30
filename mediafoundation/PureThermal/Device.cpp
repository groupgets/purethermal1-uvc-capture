#include "pch.h"
#include "Device.h"


template <class T>
void SafeRelease(T** object)
{
	if (*object)
	{
		(*object)->Release();
		*object = nullptr;
	}
}


Device::Device()
{
	if (!SelectDevice())
	{
		return;
	}
	if (!InitializeDevice())
	{
		return;
	}
	if (!InitializeXuGuidToNodeMap())
	{
		return;
	}

	if (!InitializeMediaTypes())
	{
		return;
	}

	auto hr = _videoReader->ReadSample(static_cast<DWORD>(MF_SOURCE_READER_FIRST_VIDEO_STREAM), 0, nullptr, nullptr, nullptr, nullptr);
	CheckResult(hr, "Asking for first sample");
}


Device::~Device()
{
	for (UINT32 i = 0; i < _numberOfAvailableVideoDevices; ++i)
	{
		SafeRelease(&(_availableVideoDevices[i]));
	}
	CoTaskMemFree(_availableVideoDevices);
}


void Device::PrintDeviceInfo()
{
	LepOemSwVersion version{};
	char flir_pn[32];
	char flir_sn[8];
	SetGetExtensionUnit(_xuLepOem, 9, KSPROPERTY_TYPE_GET, &version, sizeof(version));
	SetGetExtensionUnit(_xuLepOem, 8, KSPROPERTY_TYPE_GET, flir_pn, sizeof(flir_pn));
	SetGetExtensionUnit(_xuLepSys, 3, KSPROPERTY_TYPE_GET, flir_sn, sizeof(flir_sn));
	std::cout
		<< "Version gpp: "
		<< static_cast<unsigned int>(version.gpp_major) << "."
		<< static_cast<unsigned int>(version.gpp_minor) << "."
		<< static_cast<unsigned int>(version.gpp_build)
		<< " dsp: "
		<< static_cast<unsigned int>(version.dsp_major) << "."
		<< static_cast<unsigned int>(version.dsp_minor) << "."
		<< static_cast<unsigned int>(version.dsp_build) << "\n"
		<< "FLIR part#: " << flir_pn << "\n"
		<< "FLIR serial#: ";
	for (size_t i = 0; i < sizeof(flir_sn); ++i)
	{
		if (i != 0)
		{
			std::cout << "-";
		}
		std::cout << static_cast<unsigned int>(flir_sn[i]);
	}
	std::cout << "\n";
}


Device::Frame Device::GetFrame()
{
	if (_mediaTypes.empty())
	{
		// no Y16 media types available -> return empty frame buffer
		return _frameBuffer;
	}
	using namespace std::chrono_literals;
	std::unique_lock<std::mutex> lock{ _deviceMutex };
	_frameRequested = true;
	_deviceCondition.wait_for(lock, 5s, [this]() { return !_frameRequested; });
	return _frameBuffer;
}


void Device::PerformFFC()
{
	std::uint8_t dummyData{ 0 };  // 1-byte data required by interface, but ignored for Lepton CCI Run commands
	SetGetExtensionUnit(_xuLepSys, 17, KSPROPERTY_TYPE_SET, &dummyData, sizeof(dummyData));
}


// method from IUnknown
STDMETHODIMP Device::QueryInterface(REFIID riid, void** ppvObject)
{
	static const QITAB qit[] = { QITABENT(Device, IMFSourceReaderCallback), { 0 }, };
	return QISearch(this, qit, riid, ppvObject);
}


// method from IUnknown
ULONG Device::Release()
{
	auto count = InterlockedDecrement(&_referenceCount);
	if (count == 0)
	{
		delete this;
	}
	// For thread safety
	return count;
}


// method from IUnknown
ULONG Device::AddRef()
{
	return InterlockedIncrement(&_referenceCount);
}


// method from IMFSourceReaderCallback
STDMETHODIMP Device::OnEvent(DWORD, IMFMediaEvent *)
{
	return S_OK;
}


// method from IMFSourceReaderCallback
STDMETHODIMP Device::OnFlush(DWORD)
{
	return S_OK;
}


bool Device::SelectDevice()
{
	// Create an attribute store to specify the enumeration parameters.
	CComPtr<IMFAttributes> pVideoConfig{ nullptr };
	HRESULT hr = MFCreateAttributes(&pVideoConfig, 1);
	CheckResult(hr, "Create attribute store");

	// Source type: video capture devices
	hr = pVideoConfig->SetGUID(
		MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE,
		MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE_VIDCAP_GUID
	);
	CheckResult(hr, "Video capture device SetGUID");

	// Enumerate devices.
	hr = MFEnumDeviceSources(pVideoConfig, &_availableVideoDevices, &_numberOfAvailableVideoDevices);
	CheckResult(hr, "Device enumeration");

	for (UINT32 i = 0; i < _numberOfAvailableVideoDevices; ++i)
	{
		UINT32 cchName;
		WCHAR* szDevicePath;
		hr = _availableVideoDevices[i]->GetAllocatedString(
			MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE_VIDCAP_SYMBOLIC_LINK,
			&szDevicePath, &cchName);
		auto sDevicePath = WCharToString(szDevicePath);
		CoTaskMemFree(szDevicePath);
		CheckResult(hr, "Get video device path");
		if (sDevicePath.find("vid_1e4e&pid_0100") != std::string::npos)
		{
			_selectedDeviceIndex = i;
			break;
		}
	}

	if (_selectedDeviceIndex != (std::numeric_limits<UINT32>::max)())
	{
		return true;
	}
	else
	{
		return false;
	}
}


bool Device::InitializeDevice()
{
	try
	{
		CComPtr<IMFAttributes> attributes{ nullptr };
		std::lock_guard<std::mutex>{ _deviceMutex };

		auto hr = _availableVideoDevices[_selectedDeviceIndex]->ActivateObject(IID_PPV_ARGS(&_videoSource));
		CheckResult(hr, "Activating video device");

		hr = MFCreateAttributes(&attributes, 2);
		CheckResult(hr, "Allocate device attributes");

		hr = attributes->SetUINT32(MF_READWRITE_DISABLE_CONVERTERS, TRUE);
		CheckResult(hr, "Get device attributes");

		hr = attributes->SetUnknown(MF_SOURCE_READER_ASYNC_CALLBACK, this);
		CheckResult(hr, "Set device callback pointer");

		hr = MFCreateSourceReaderFromMediaSource(_videoSource, attributes, &_videoReader);
		CheckResult(hr, "Creating video source reader");

		return true;
	}
	catch (const std::exception&)
	{
		return false;
	}
}


bool Device::InitializeXuGuidToNodeMap()
{
	GUID nodeType;
	CComPtr<IKsTopologyInfo> ksTopologyInfo{ nullptr };
	CComPtr<IUnknown> unknown{ nullptr };
	CComPtr<IKsControl> ksControl{ nullptr };
	KSP_NODE kspNode;
	kspNode.Property.Id = KSPROPERTY_EXTENSION_UNIT_INFO;
	kspNode.Property.Flags = KSPROPERTY_TYPE_GET | KSPROPERTY_TYPE_TOPOLOGY;

	auto hr = _videoSource->QueryInterface(__uuidof(IKsTopologyInfo), reinterpret_cast<void**>(&ksTopologyInfo));
	CheckResult(hr, "IMFMediaSource::QueryInterface(IKsTopologyInfo)");

	std::vector<std::reference_wrapper<const XuGuid> > xuGuids{ _xuLepOem , _xuLepSys };
	DWORD numNodes{ 0 };
	hr = ksTopologyInfo->get_NumNodes(&numNodes);
	CheckResult(hr, "ks_topology_info->get_NumNodes(...)");
	ULONG dummyLen;
	for (DWORD iNode = 0; iNode < numNodes; ++iNode, unknown = nullptr, ksControl = nullptr)
	{
		hr = ksTopologyInfo->get_NodeType(iNode, &nodeType);
		CheckResult(hr, "ks_topology_info->get_NodeType(...)");
		if (KSNODETYPE_DEV_SPECIFIC != nodeType)  // extension unit nodes are device-specific nodes
		{
			continue;
		}

		kspNode.NodeId = static_cast<ULONG>(iNode);

		hr = ksTopologyInfo->CreateNodeInstance(iNode, IID_IUnknown, reinterpret_cast<void**>(&unknown));
		CheckResult(hr, "ks_topology_info->CreateNodeInstance(...)");

		hr = unknown->QueryInterface(__uuidof(IKsControl), reinterpret_cast<void**>(&ksControl));
		CheckResult(hr, "ks_topology_info->QueryInterface(...)");

		for (auto itGuid = xuGuids.cbegin(); itGuid != xuGuids.cend(); ++itGuid)
		{
			kspNode.Property.Set = *reinterpret_cast<const GUID*>(itGuid->get().data());

			hr = ksControl->KsProperty(reinterpret_cast<PKSPROPERTY>(&kspNode), sizeof(kspNode), nullptr, 0, &dummyLen);
			if (HRESULT_FROM_WIN32(ERROR_SET_NOT_FOUND) == hr)
			{
				continue;
			}
			else if (HRESULT_FROM_WIN32(ERROR_MORE_DATA) == hr) // expected behaviour because we provided a DataLength of 0
			{
				_guidToNodeIdMap[itGuid->get()] = iNode;
				xuGuids.erase(itGuid);
			}
			else
			{
				CheckResult(hr, "pKsControl->KsProperty(...)");
			}
			break;
		}

		if (xuGuids.empty()) // found all required extension unit nodes --> skip further nodes
		{
			break;
		}
	}
	if (_guidToNodeIdMap.empty())
	{
		return false;
	}
	else
	{
		return true;
	}
}


bool Device::InitializeMediaTypes()
{
	_mediaTypes.clear();
	auto hr = _videoSource->CreatePresentationDescriptor(&_presentationDescriptor);
	CheckResult(hr, "Creating presentation descriptor");

	DWORD nStreamDescriptors;
	_presentationDescriptor->GetStreamDescriptorCount(&nStreamDescriptors);
	CheckResult(hr, "Get stream descriptor count");
	for (DWORD iStream = 0; iStream < nStreamDescriptors; ++iStream)
	{
		BOOL fSelected;
		hr = _presentationDescriptor->GetStreamDescriptorByIndex(iStream, &fSelected, &_streamDescriptor);
		CheckResult(hr, "Get stream descriptor");

		hr = _streamDescriptor->GetMediaTypeHandler(&_mediaTypeHandler);
		CheckResult(hr, "Get media type handler");

		DWORD nTypes;
		hr = _mediaTypeHandler->GetMediaTypeCount(&nTypes);
		CheckResult(hr, "Get media type count");

		for (DWORD iType = 0; iType < nTypes; ++iType, _mediaType = nullptr)
		{
			hr = _mediaTypeHandler->GetMediaTypeByIndex(iType, &_mediaType);
			CheckResult(hr, "Get media type");
			GUID pSubType;
			hr = _mediaType->GetGUID(MF_MT_SUBTYPE, &pSubType);
			CheckResult(hr, "Get sub type");
			if (std::memcmp(_y16FourCC.data(), &(pSubType.Data1), _y16FourCC.size()) == 0)
			{
				_mediaTypes.push_back(_mediaType);
			}
		}
	}

	if (_mediaTypes.empty())
	{
		return false;
	}

	int telemetryIndex{ -1 };
	UINT32 minHeight{ (std::numeric_limits<UINT32>::max)() };
	UINT32 maxHeight{ 0 };
	UINT32 width{ 0 };
	UINT32 height{ 0 };
	for (size_t i = 0; i < _mediaTypes.size(); ++i)
	{
		hr = MFGetAttributeSize(_mediaTypes[i], MF_MT_FRAME_SIZE, &width, &height);
		CheckResult(hr, "get frame size");
		if (height > maxHeight)
		{
			maxHeight = height;
			telemetryIndex = static_cast<int>(i);
		}
		if (height < minHeight)
		{
			minHeight = height;
		}
	}
	_numberOfTelemetryRows = maxHeight - minHeight;
	if (_numberOfTelemetryRows == 0)
	{
		telemetryIndex = -1;
	}
	_mediaType = _mediaTypes[_numberOfTelemetryRows > 0 ? telemetryIndex : 0];
	_frameBuffer.width = width;
	_frameBuffer.height = minHeight;
	_frameBuffer.data.resize(_frameBuffer.width * _frameBuffer.height);
	hr = _videoReader->SetCurrentMediaType(MF_SOURCE_READER_FIRST_VIDEO_STREAM, nullptr, _mediaType);
	CheckResult(hr, "set media type");
	return true;
}


bool Device::ExtractTelemetryData(const std::uint16_t * telemetryData)
{
	switch (_numberOfTelemetryRows)
	{
	case 0:
		return true;
	case 2: // lepton 3: resolution 160x120 -> 3 telemetry data packets fit in 2 rows
	case 3: // lepton 2: resolution 80x60   -> 3 telemetry data packets fit in 3 rows
	{
		// details on telemetry data encoding and video packet payload length (80 * sizeof(uint16_t) = 160 bytes) taken from here:
		// https://www.flir.de/globalassets/imported-assets/document/flir-lepton-engineering-datasheet.pdf
		static constexpr size_t packetPayloadLength{ 80 };
		auto oStatusBits = std::bitset<16>(*(telemetryData + 3));
		const bool ffcInProgress = oStatusBits[4] == 1 && oStatusBits[5] == 0;
		if (ffcInProgress)
		{
			return false;
		}
		_frameBuffer.fpaTemp = *(telemetryData + 24);
		_frameBuffer.housingTemp = *(telemetryData + 26);
		_frameBuffer.spotmeterMean = *(telemetryData + 2 * packetPayloadLength + 50);
		return true;
	}
	default:
		throw std::runtime_error("unsupported telemetry data format");
	}
}


void Device::CheckResult(HRESULT hResult, const std::string & crsDescription)
{
	if (FAILED(hResult))
	{
		std::stringstream ssMessage;
		ssMessage << crsDescription << ": failed, error code: " << hResult;
		throw std::runtime_error(ssMessage.str());
	}
}


std::string Device::WCharToString(const WCHAR * str)
{
	auto length = WideCharToMultiByte(CP_UTF8, 0, str, -1, nullptr, 0, nullptr, nullptr);
	if (length == 0)
	{
		std::stringstream message;
		message << "WideCharToMultiByte(...) returned 0 and GetLastError() is " << GetLastError();
		throw std::runtime_error(message.str());
	}

	std::string buffer(length - 1, ' ');
	length = WideCharToMultiByte(CP_UTF8, 0, str, -1, &buffer[0], static_cast<int>(buffer.size()) + 1, nullptr, nullptr);
	if (length == 0)
	{
		std::stringstream message;
		message << "WideCharToMultiByte(...) returned 0 and GetLastError() is " << GetLastError();
		throw std::runtime_error(message.str());
	}

	return buffer;
}


void Device::SetGetExtensionUnit(const XuGuid& xuGuid, ULONG xuControlId, ULONG xuRequestType, void * data, ULONG len)
{
	if (!_videoSource)
	{
		return;
	}

	const auto itXuNodeId = _guidToNodeIdMap.find(xuGuid);
	if (itXuNodeId == _guidToNodeIdMap.end())
	{
		throw std::runtime_error("Unknown extension unit");
	}

	HRESULT hr{ S_OK };
	CComPtr<IKsTopologyInfo> ksTopologyInfo{ nullptr };
	CComPtr<IUnknown> unknown{ nullptr };
	CComPtr<IKsControl> ksControl{ nullptr };
	KSP_NODE kspNode;

	hr = _videoSource->QueryInterface(__uuidof(IKsTopologyInfo), reinterpret_cast<void**>(&ksTopologyInfo));
	CheckResult(hr, "IMFMediaSource::QueryInterface(IKsTopologyInfo)");

	hr = ksTopologyInfo->CreateNodeInstance(itXuNodeId->second, IID_IUnknown, reinterpret_cast<void**>(&unknown));
	CheckResult(hr, "ks_topology_info->CreateNodeInstance(...)");

	hr = unknown->QueryInterface(__uuidof(IKsControl), reinterpret_cast<void**>(&ksControl));
	CheckResult(hr, "ks_topology_info->QueryInterface(...)");

	kspNode.Property.Set = *reinterpret_cast<const GUID*>(xuGuid.data());
	kspNode.NodeId = static_cast<ULONG>(itXuNodeId->second);
	kspNode.Property.Id = xuControlId;
	kspNode.Property.Flags = xuRequestType | KSPROPERTY_TYPE_TOPOLOGY;

	hr = ksControl->KsProperty(reinterpret_cast<PKSPROPERTY>(&kspNode), sizeof(kspNode), data, len, &len);
	CheckResult(hr, "ks_control->KsProperty(...)");
}


// method from IMFSourceReaderCallback
HRESULT Device::OnReadSample(HRESULT status, DWORD streamIndex, DWORD streamFlags, LONGLONG timeStamp, IMFSample * sample)
{
	HRESULT hr{ S_OK };
	CComPtr<IMFMediaBuffer> mediaBuffer{ nullptr };

	{
		std::lock_guard<std::mutex>{ _deviceMutex };

		if (FAILED(status))
		{
			hr = status;
		}

		if (SUCCEEDED(hr) && sample && _frameRequested)
		{
			// Get the video frame sBuffer from the pSample.
			hr = sample->GetBufferByIndex(0, &mediaBuffer);
			// Retrieve the frame.
			if (SUCCEEDED(hr))
			{
				BYTE* data;
				mediaBuffer->Lock(&data, nullptr, nullptr);
				if (ExtractTelemetryData(reinterpret_cast<std::uint16_t*>(data) + _frameBuffer.data.size()))
				{
					CopyMemory(_frameBuffer.data.data(), data, _frameBuffer.data.size() * sizeof(std::uint16_t));
					_frameRequested = false;
				}
			}
		}
	}
	_deviceCondition.notify_one();

	// Request the next frame.
	if (SUCCEEDED(hr))
	{
		hr = _videoReader->ReadSample(static_cast<DWORD>(MF_SOURCE_READER_FIRST_VIDEO_STREAM), 0, nullptr, nullptr, nullptr, nullptr);
	}

	if (FAILED(hr))
	{
		//Notify there was an error
		PostMessage(nullptr, 1, static_cast<WPARAM>(hr), 0L);
	}

	return hr;
}
