"""
This will log into a juniper device (Currently filtered to qfx's by the main program that calls it)
But this should work with MX devices as well.

This will run the following command and process the xml output (Sample below).
show interfaces diagnostics optics | display xml

        <physical-interface>
            <name>xe-0/0/1</name>
            <optics-diagnostics>
                <laser-bias-current>33.054</laser-bias-current>
                <laser-output-power>0.5180</laser-output-power>
                <laser-output-power-dbm>-2.86</laser-output-power-dbm>
                <module-temperature junos:celsius="34.8">35 degrees C / 95 degrees F</module-temperature>
                <module-voltage>3.2870</module-voltage>
                <rx-signal-avg-optical-power>0.5634</rx-signal-avg-optical-power>
                <rx-signal-avg-optical-power-dbm>-2.49</rx-signal-avg-optical-power-dbm>
                <laser-bias-current-high-alarm>off</laser-bias-current-high-alarm>
                <laser-bias-current-low-alarm>off</laser-bias-current-low-alarm>
                <laser-bias-current-high-warn>off</laser-bias-current-high-warn>
                <laser-bias-current-low-warn>off</laser-bias-current-low-warn>
                <laser-tx-power-high-alarm>off</laser-tx-power-high-alarm>
                <laser-tx-power-low-alarm>off</laser-tx-power-low-alarm>
                <laser-tx-power-high-warn>off</laser-tx-power-high-warn>
                <laser-tx-power-low-warn>off</laser-tx-power-low-warn>
                <module-temperature-high-alarm>off</module-temperature-high-alarm>
                <module-temperature-low-alarm>off</module-temperature-low-alarm>
                <module-temperature-high-warn>off</module-temperature-high-warn>
                <module-temperature-low-warn>off</module-temperature-low-warn>
                <module-voltage-high-alarm>off</module-voltage-high-alarm>
                <module-voltage-low-alarm>off</module-voltage-low-alarm>
                <module-voltage-high-warn>off</module-voltage-high-warn>
                <module-voltage-low-warn>off</module-voltage-low-warn>
                <laser-rx-power-high-alarm>off</laser-rx-power-high-alarm>
                <laser-rx-power-low-alarm>off</laser-rx-power-low-alarm>
                <laser-rx-power-high-warn>off</laser-rx-power-high-warn>
                <laser-rx-power-low-warn>off</laser-rx-power-low-warn>
                <laser-bias-current-high-alarm-threshold>100.000</laser-bias-current-high-alarm-threshold>
                <laser-bias-current-low-alarm-threshold>2.000</laser-bias-current-low-alarm-threshold>
                <laser-bias-current-high-warn-threshold>80.000</laser-bias-current-high-warn-threshold>
                <laser-bias-current-low-warn-threshold>4.000</laser-bias-current-low-warn-threshold>
                <laser-tx-power-high-alarm-threshold>1.3460</laser-tx-power-high-alarm-threshold>
                <laser-tx-power-high-alarm-threshold-dbm>1.29</laser-tx-power-high-alarm-threshold-dbm>
                <laser-tx-power-low-alarm-threshold>0.1210</laser-tx-power-low-alarm-threshold>
                <laser-tx-power-low-alarm-threshold-dbm>-9.17</laser-tx-power-low-alarm-threshold-dbm>
                <laser-tx-power-high-warn-threshold>1.1220</laser-tx-power-high-warn-threshold>
                <laser-tx-power-high-warn-threshold-dbm>0.50</laser-tx-power-high-warn-threshold-dbm>
                <laser-tx-power-low-warn-threshold>0.1510</laser-tx-power-low-warn-threshold>
                <laser-tx-power-low-warn-threshold-dbm>-8.21</laser-tx-power-low-warn-threshold-dbm>
                <module-temperature-high-alarm-threshold junos:celsius="90.0">90 degrees C / 194 degrees F
                </module-temperature-high-alarm-threshold>
                <module-temperature-low-alarm-threshold junos:celsius="-10.0">-10 degrees C / 14 degrees F</module-temperature-low-alarm-threshold>
                <module-temperature-high-warn-threshold junos:celsius="85.0">85 degrees C / 185 degrees F
                </module-temperature-high-warn-threshold>
                <module-temperature-low-warn-threshold junos:celsius="-5.0">-5 degrees C / 23 degrees F</module-temperature-low-warn-threshold>
                <module-voltage-high-alarm-threshold>3.630</module-voltage-high-alarm-threshold>
                <module-voltage-low-alarm-threshold>2.970</module-voltage-low-alarm-threshold>
                <module-voltage-high-warn-threshold>3.460</module-voltage-high-warn-threshold>
                <module-voltage-low-warn-threshold>3.130</module-voltage-low-warn-threshold>
                <laser-rx-power-high-alarm-threshold>2.0000</laser-rx-power-high-alarm-threshold>
                <laser-rx-power-high-alarm-threshold-dbm>3.01</laser-rx-power-high-alarm-threshold-dbm>
                <laser-rx-power-low-alarm-threshold>0.0158</laser-rx-power-low-alarm-threshold>
                <laser-rx-power-low-alarm-threshold-dbm>-18.01</laser-rx-power-low-alarm-threshold-dbm>
                <laser-rx-power-high-warn-threshold>1.0000</laser-rx-power-high-warn-threshold>
                <laser-rx-power-high-warn-threshold-dbm>0.00</laser-rx-power-high-warn-threshold-dbm>
                <laser-rx-power-low-warn-threshold>0.0316</laser-rx-power-low-warn-threshold>
                <laser-rx-power-low-warn-threshold-dbm>-15.00</laser-rx-power-low-warn-threshold-dbm>
            </optics-diagnostics>
        </physical-interface>

Due to some of junipers added information inside the XML, Anything that contains "junos: xyz" may fail to process correctly.
So this script is built to search the xpath expressions instead for a specific variable using the item.find commands
"""

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError

def return_interface_diagnostics_optics(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']


    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            count = 0
            output = {}
            interface_diagnostice_optics = dev.rpc.get_interface_optics_diagnostics_information()
            interface_diagnostice_optics_information = interface_diagnostice_optics.findall('.//physical-interface')
            for item in interface_diagnostice_optics_information:
                interface = item.find('.//name').text

                """
                Test to see if the following variables exist in the xml output. 
                If not then assign default values or null values
                """

                if item.find('.//optics-diagnostics/rx-signal-avg-optical-power-dbm') is not None:
                    rx_signal_avg_optical_power_dbm = item.find('.//optics-diagnostics/rx-signal-avg-optical-power-dbm').text
                else:
                    rx_signal_avg_optical_power_dbm = False

                if item.find('.//optics-diagnostics/laser-output-power-dbm') is not None:
                    laser_output_power_dbm = item.find('.//optics-diagnostics/laser-output-power-dbm').text
                else:
                    laser_output_power_dbm = False

                if item.find('.//laser-bias-current-high-alarm') is not None:
                    laser_bias_current_high_alarm = item.find('.//laser-bias-current-high-alarm').text
                else:
                    laser_bias_current_high_alarm = False

                if item.find('.//laser-bias-current-low-alarm') is not None:
                    laser_bias_current_low_alarm = item.find('.//laser-bias-current-low-alarm').text
                else:
                    laser_bias_current_low_alarm = False

                if item.find('.//laser-bias-current-high-warn') is not None:
                    laser_bias_current_high_warn = item.find('.//laser-bias-current-high-warn').text
                else:
                    laser_bias_current_high_warn = False

                if item.find('.//laser-bias-current-low-warn') is not None:
                    laser_bias_current_low_warn = item.find('.//laser-bias-current-low-warn').text
                else:
                    laser_bias_current_low_warn = False

                if item.find('.//laser-tx-power-high-alarm') is not None:
                    laser_tx_power_high_alarm = item.find('.//laser-tx-power-high-alarm').text
                else:
                    laser_tx_power_high_alarm = False

                if item.find('.//laser-tx-power-low-alarm') is not None:
                    laser_tx_power_low_alarm = item.find('.//laser-tx-power-low-alarm').text
                else:
                    laser_tx_power_low_alarm = False

                if item.find('.//laser-tx-power-high-warn') is not None:
                    laser_tx_power_high_warn = item.find('.//laser-tx-power-high-warn').text
                else:
                    laser_tx_power_high_warn = False

                if item.find('.//laser-tx-power-low-warn') is not None:
                    laser_tx_power_low_warn = item.find('.//laser-tx-power-low-warn').text
                else:
                    laser_tx_power_low_warn = False

                if item.find('.//module-temperature-high-alarm') is not None:
                    module_temperature_high_alarm = item.find('.//module-temperature-high-alarm').text
                else:
                    module_temperature_high_alarm = False

                if item.find('.//module-temperature-high-warn') is not None:
                    module_temperature_high_warn = item.find('.//module-temperature-high-warn').text
                else:
                    module_temperature_high_warn = False

                if item.find('.//module-temperature-low-warn') is not None:
                    module_temperature_low_warn = item.find('.//module-temperature-low-warn').text
                else:
                    module_temperature_low_warn = False

                if item.find('.//module-voltage-high-alarm') is not None:
                    module_voltage_high_alarm = item.find('.//module-voltage-high-alarm').text
                else:
                    module_voltage_high_alarm = False

                if item.find('.//module-voltage-low-alarm') is not None:
                    module_voltage_low_alarm = item.find('.//module-voltage-low-alarm').text
                else:
                    module_voltage_low_alarm = False

                if item.find('.//module-voltage-high-warn') is not None:
                    module_voltage_high_warn = item.find('.//module-voltage-high-warn').text
                else:
                    module_voltage_high_warn = False

                if item.find('.//module-voltage-low-warn') is not None:
                    module_voltage_low_warn = item.find('.//module-voltage-low-warn').text
                else:
                    module_voltage_low_warn = False

                if item.find('.//laser-rx-power-high-alarm-threshold-dbm') is not None:
                    laser_rx_power_high_alarm_threshold_dbm = item.find('.//laser-rx-power-high-alarm-threshold-dbm').text
                else:
                    laser_rx_power_high_alarm_threshold_dbm = False

                if item.find('.//laser-rx-power-low-alarm-threshold-dbm') is not None:
                    laser_rx_power_low_alarm_threshold_dbm = item.find('.//laser-rx-power-low-alarm-threshold-dbm').text
                else:
                    laser_rx_power_low_alarm_threshold_dbm = False

                if item.find('.//laser-rx-power-high-warn-threshold-dbm') is not None:
                    laser_rx_power_high_warn_threshold_dbm = item.find('.//laser-rx-power-high-warn-threshold-dbm').text
                else:
                    laser_rx_power_high_warn_threshold_dbm = False

                if item.find('.//laser-rx-power-low-warn-threshold-dbm') is not None:
                    laser_rx_power_low_warn_threshold_dbm = item.find('.//laser-rx-power-low-warn-threshold-dbm').text
                else:
                    laser_rx_power_low_warn_threshold_dbm = False

                if item.find('.//laser-rx-power-high-alarm') is not None:
                    laser_rx_power_high_alarm = item.find('.//laser-rx-power-high-alarm').text
                else:
                    laser_rx_power_high_alarm = False

                if item.find('.//laser-rx-power-low-alarm') is not None:
                    laser_rx_power_low_alarm = item.find('.//laser-rx-power-low-alarm').text
                else:
                    laser_rx_power_low_alarm = False

                if item.find('.//laser-rx-power-high-warn') is not None:
                    laser_rx_power_high_warn = item.find('.//laser-rx-power-high-warn').text
                else:
                    laser_rx_power_high_warn = False

                if item.find('.//laser-rx-power-low-warn') is not None:
                    laser_rx_power_low_warn = item.find('.//laser-rx-power-low-warn').text
                else:
                    laser_rx_power_low_warn = False

                if item.findall('.//lane-index') is not None:
                    lane_index = []
                    for lane_item in item.findall('.//lane-index'):
                        lane_index.append(lane_item.text)
                else:
                    lane_index = False

                if item.findall('.//optics-diagnostics/optics-diagnostics-lane-values/laser-output-power-dbm') is not None:
                    laser_output_power_dbm_lanes = []
                    for output_power_dbm_lanes in item.findall('.//optics-diagnostics/optics-diagnostics-lane-values/laser-output-power-dbm'):
                        laser_output_power_dbm_lanes.append(output_power_dbm_lanes.text)
                else:
                    laser_output_power_dbm_lanes = False

                if item.findall('.//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-optical-power-dbm') is not None:
                    laser_rx_optical_power_dbm_lanes = []
                    for rx_power_dbm_lanes in item.findall('.//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-optical-power-dbm'):
                        laser_rx_optical_power_dbm_lanes.append(rx_power_dbm_lanes.text)
                else:
                    laser_rx_optical_power_dbm_lanes = False

                output[count] = {}
                output[count] = {'interface': interface,
                                 'rx_signal_avg_optical_power_dbm': rx_signal_avg_optical_power_dbm,
                                 'laser_output_power_dbm': laser_output_power_dbm,
                                 'lane_index': lane_index,
                                 'laser_output_power_dbm_lanes': laser_output_power_dbm_lanes,
                                 'laser_rx_optical_power_dbm_lanes': laser_rx_optical_power_dbm_lanes,
                                 'laser_rx_power_high_alarm_threshold_dbm': laser_rx_power_high_alarm_threshold_dbm,
                                 'laser_rx_power_low_alarm_threshold_dbm': laser_rx_power_low_alarm_threshold_dbm,
                                 'laser_rx_power_high_warn_threshold_dbm': laser_rx_power_high_warn_threshold_dbm,
                                 'laser_rx_power_low_warn_threshold_dbm': laser_rx_power_low_warn_threshold_dbm,
                                 'laser_bias_current_high_alarm': laser_bias_current_high_alarm,
                                 'laser_bias_current_low_alarm': laser_bias_current_low_alarm,
                                 'laser_bias_current_high_warn': laser_bias_current_high_warn,
                                 'laser_bias_current_low_warn': laser_bias_current_low_warn,
                                 'laser_tx_power_high_alarm': laser_tx_power_high_alarm,
                                 'laser_tx_power_low_alarm': laser_tx_power_low_alarm,
                                 'laser_tx_power_high_warn': laser_tx_power_high_warn,
                                 'laser_tx_power_low_warn': laser_tx_power_low_warn,
                                 'module_temperature_high_alarm': module_temperature_high_alarm,
                                 'module_temperature_high_warn': module_temperature_high_warn,
                                 'module_temperature_low_warn': module_temperature_low_warn,
                                 'module_voltage_high_alarm': module_voltage_high_alarm,
                                 'module_voltage_low_alarm': module_voltage_low_alarm,
                                 'module_voltage_high_warn': module_voltage_high_warn,
                                 'module_voltage_low_warn': module_voltage_low_warn,
                                 'laser_rx_power_high_alarm': laser_rx_power_high_alarm,
                                 'laser_rx_power_low_alarm': laser_rx_power_low_alarm,
                                 'laser_rx_power_high_warn': laser_rx_power_high_warn,
                                 'laser_rx_power_low_warn': laser_rx_power_low_warn}
                count += 1

            return output
        except ConnectError as err:
            sys.stdout.write("Error")
            sys.stdout.flush()
            sys.exit(0)