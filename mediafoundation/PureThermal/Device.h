#pragma once

#include <algorithm>
#include <array>
#include <atomic>
#include <bitset>
#include <condition_variable>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <mutex>
#include <sstream>
#include <vector>

#include <atlcomcli.h>
#include <mfapi.h>
#include <mferror.h>
#include <mfplay.h>
#include <mfreadwrite.h>
#include <mmsystem.h>
#include <ks.h>
#include <ksproxy.h>
#include <ksmedia.h>
#include <vidcap.h>
#include <shlwapi.h>

#include "LEPTON_Types.h"


class Device : public IMFSourceReaderCallback
{
public:
	struct Frame
	{
		std::vector<std::uint16_t> data;
		std::size_t width{ 0 };
		std::size_t height{ 0 };
		std::uint16_t fpaTemp{ 0 };
		std::uint16_t housingTemp{ 0 };
		std::uint16_t spotmeterMean{ 0 };
	};

	Device();
	virtual ~Device();
	operator bool() const { return _videoSource; }

	void PrintDeviceInfo();
	Frame GetFrame();
	void PerformFFC();

	// the class must implement the methods from IUnknown
	STDMETHODIMP QueryInterface(REFIID iid, void** ppv);
	STDMETHODIMP_(ULONG) AddRef();
	STDMETHODIMP_(ULONG) Release();

	//  the class must implement the methods from IMFSourceReaderCallback
	STDMETHODIMP OnReadSample(HRESULT status, DWORD streamIndex, DWORD streamFlags, LONGLONG timeStamp, IMFSample*);
	STDMETHODIMP OnEvent(DWORD, IMFMediaEvent *);
	STDMETHODIMP OnFlush(DWORD);

	/*
	Returns the camera status as a string. Status is based on FLIR LEP_SYSTEM_STATUS_STATES_E_TAG and can be:

		LEP_SYSTEM_READY -> Ready
		LEP_SYSTEM_INITIALIZING -> Initializing
		LEP_SYSTEM_IN_LOW_POWER_MODE -> In low power mode
		LEP_SYSTEM_GOING_INTO_STANDBY -> Going into standby
		LEP_SYSTEM_FLAT_FIELD_IN_PROCESS -> Flat field in process

		Default is "N/A"
	*/
	std::string GetFLIRStatus();

private:
	using XuGuid = std::array<std::uint8_t, 16>;
	using FourCC = std::array<std::uint8_t, 4>;

	struct LepOemSwVersion
	{
		std::uint8_t gpp_major{ 0 };
		std::uint8_t gpp_minor{ 0 };
		std::uint8_t gpp_build{ 0 };
		std::uint8_t dsp_major{ 0 };
		std::uint8_t dsp_minor{ 0 };
		std::uint8_t dsp_build{ 0 };
		std::uint16_t reserved{ 0 };
	};

	bool SelectDevice();
	bool InitializeDevice();
	bool InitializeXuGuidToNodeMap();
	bool InitializeMediaTypes();
	bool ExtractTelemetryData(const std::uint16_t* telemetryData);

	static void CheckResult(HRESULT, const std::string& crsDescription);
	static std::string WCharToString(const WCHAR*);
	void SetGetExtensionUnit(const XuGuid& xuGuid, ULONG xuControlId, ULONG xuRequestType, void* data, ULONG len);

	static constexpr FourCC _y16FourCC{ {'Y', '1', '6', ' '} };
	static constexpr XuGuid _xuLepOem{ { 'p','t','1','-','l','e','p','-','o','e','m','-','0','0','0','0' } };
	static constexpr XuGuid _xuLepSys{ { 'p','t','1','-','l','e','p','-','s','y','s','-','0','0','0','0' } };

	CComPtr<IMFMediaSource> _videoSource{ nullptr };
	CComPtr<IMFSourceReader> _videoReader{ nullptr };
	IMFActivate** _availableVideoDevices{ nullptr };
	UINT32 _numberOfAvailableVideoDevices{ 0 };
	UINT32 _selectedDeviceIndex{ (std::numeric_limits<UINT32>::max)() };
	std::string _selectedDeviceID;

	CComPtr<IMFPresentationDescriptor> _presentationDescriptor{ nullptr };
	CComPtr<IMFStreamDescriptor> _streamDescriptor{ nullptr };
	CComPtr<IMFMediaTypeHandler> _mediaTypeHandler{ nullptr };
	std::vector<CComPtr<IMFMediaType> > _mediaTypes;
	CComPtr<IMFMediaType> _mediaType{ nullptr };

	std::map<const XuGuid, DWORD> _guidToNodeIdMap;
	Frame _frameBuffer;
	UINT32 _numberOfTelemetryRows{ 0 };

	long _referenceCount{ 1 };
	std::mutex _deviceMutex;
	std::condition_variable _deviceCondition;
	std::atomic<bool> _frameRequested{ false };

	LEP_STATUS_T_PTR flir_status;
	LEP_UINT32 flir_uptime_ms; //in Milliseconds
};
