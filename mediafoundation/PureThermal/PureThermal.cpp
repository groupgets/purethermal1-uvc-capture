#include "pch.h"
#include "Device.h"


double KelvinToCelsius(std::uint16_t kelvin)
{
	return kelvin / 100.0 - 273.15;
}

int main()
{
	auto hr = CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED | COINIT_DISABLE_OLE1DDE);
	if (FAILED(hr))
	{
		return -1;
	}
	hr = MFStartup(MF_VERSION);
	if (FAILED(hr))
	{
		CoUninitialize();
		return -1;
	}

	{
		Device pureThermal{};
		if (!pureThermal)
		{
			std::cout << "\nDid not find \"PureThermal\" device\n";
		}
		else
		{
			std::cout << "\nFound \"PureThermal\" device\n\n";

			pureThermal.PrintDeviceInfo();

			std::cout << "\nPress any key to perform an FFC..." << std::endl;
			std::cin.get();
			pureThermal.PerformFFC();

			std::cout << "Press any key to capture a frame..." << std::endl;
			std::cin.get();
			auto frame = pureThermal.GetFrame();
			if (!(frame.data.empty()))
			{
				std::stringstream fileName;
				fileName << "image_" << frame.width << "x" << frame.height << "_Y16.dat";
				const auto minValue = *std::min_element(frame.data.cbegin(), frame.data.cend());
				const auto maxValue = *std::max_element(frame.data.cbegin(), frame.data.cend());
				std::cout << "Received frame (" << fileName.str() << "):" << std::endl;
				std::cout << "\twidth:  " << frame.width << std::endl;
				std::cout << "\theight: " << frame.height << std::endl;
				std::cout << "\tminimum value: " << minValue << " (" << std::fixed << std::setprecision(2) << KelvinToCelsius(minValue) << "\370C)" << std::endl;
				std::cout << "\tmaximum value: " << maxValue << " (" << std::fixed << std::setprecision(2) << KelvinToCelsius(maxValue) << "\370C)" << std::endl;
				if (frame.fpaTemp > 0)
				{
					std::cout << "\tFPA temperature:     " << frame.fpaTemp << " (" << std::fixed << std::setprecision(2) << KelvinToCelsius(frame.fpaTemp) << "\370C)" << std::endl;
					std::cout << "\thousing temperature: " << frame.housingTemp << " (" << std::fixed << std::setprecision(2) << KelvinToCelsius(frame.housingTemp) << "\370C)" << std::endl;
					std::cout << "\tspotmeter mean:      " << frame.spotmeterMean << " (" << std::fixed << std::setprecision(2) << KelvinToCelsius(frame.spotmeterMean) << "\370C)" << std::endl;
				}
				std::ofstream outputFile{ fileName.str(), std::ios::out | std::ios::binary };
				outputFile.write(reinterpret_cast<const char*>(frame.data.data()), frame.data.size() * sizeof(decltype(frame.data)::value_type));
			}
			else
			{
				std::cout << "Y16 format not supported" << std::endl;
			}
		}
	}

	MFShutdown();
	CoUninitialize();

	std::cout << "\nPress any key to quit..." << std::endl;
	std::cin.get();
}
