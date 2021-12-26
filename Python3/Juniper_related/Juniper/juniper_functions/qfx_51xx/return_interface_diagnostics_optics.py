import yaml
from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.factory.factory_loader import FactoryLoader

def return_interface_diagnostics_optics(**kwargs):

    device_ip = kwargs['device_ip']
    username = kwargs['user']
    password = kwargs['password']
    table_view = kwargs['table_view']

    with Device(host=device_ip, user=username, password=password, gather_facts=False, normalize=True) as dev:
        try:
            output = {}
            globals().update(FactoryLoader().load(yaml.load(table_view, Loader=yaml.FullLoader)))
            diag = interfaceDiagnosticsOptics(dev)
            diag.get()
            count = 0
            for item in diag:
                output[count] = {}
                output[count] = {'interface': item.name,
                                 'laser_output_power_dbm': item.laser_output_power_dbm,
                                 'rx_signal_avg_optical_power_dbm': item.rx_signal_avg_optical_power_dbm,
                                 'laser_bias_current_high_alarm': item.laser_bias_current_high_alarm,
                                 'laser_bias_current_low_alarm': item.laser_bias_current_low_alarm,
                                 'laser_bias_current_high_warn': item.laser_bias_current_high_warn,
                                 'laser_bias_current_low_warn': item.laser_bias_current_low_warn,
                                 'laser_tx_power_high_alarm': item.laser_tx_power_high_alarm,
                                 'laser_tx_power_low_alarm': item.laser_tx_power_low_alarm,
                                 'laser_tx_power_high_warn': item.laser_tx_power_high_warn,
                                 'laser_tx_power_low_warn': item.laser_tx_power_low_warn,
                                 'module_temperature_high_alarm': item.module_temperature_high_alarm,
                                 'module_temperature_high_warn': item.module_temperature_high_warn,
                                 'module_temperature_low_warn': item.module_temperature_low_warn,
                                 'module_voltage_high_alarm': item.module_voltage_high_alarm,
                                 'module_voltage_low_alarm': item.module_voltage_low_alarm,
                                 'module_voltage_high_warn': item.module_voltage_high_warn,
                                 'module_voltage_low_warn': item.module_voltage_low_warn,
                                 'laser_rx_power_high_alarm': item.laser_rx_power_high_alarm,
                                 'laser_rx_power_low_alarm': item.laser_rx_power_low_alarm,
                                 'laser_rx_power_low_warn': item.laser_rx_power_low_warn,
                                 'lane_index': item.lane_index,
                                 'laser_output_power_dbm_lanes': item.laser_output_power_dbm_lanes,
                                 'laser_rx_optical_power_dbm_lanes': item.laser_rx_optical_power_dbm_lanes,
                                 'laser_bias_current_high_alarm_lanes': item.laser_bias_current_high_alarm_lanes,
                                 'laser_bias_current_low_alarm_lanes': item.laser_bias_current_low_alarm_lanes,
                                 'laser_bias_current_high_warn_lanes': item.laser_bias_current_high_warn_lanes,
                                 'laser_bias_current_low_warn_lanes': item.laser_bias_current_low_warn_lanes,
                                 'laser_rx_power_high_alarm_lanes': item.laser_rx_power_high_alarm_lanes,
                                 'laser_rx_power_low_alarm_lanes': item.laser_rx_power_low_alarm_lanes,
                                 'laser_rx_power_high_warn_lanes': item.laser_rx_power_high_warn_lanes,
                                 'laser_rx_power_low_warn_lanes': item.laser_rx_power_low_warn_lanes,
                                 'tx_loss_of_signal_functionality_alarm_lanes': item.tx_loss_of_signal_functionality_alarm_lanes,
                                 'rx_loss_of_signal_alarm_lanes': item.rx_loss_of_signal_alarm_lanes,
                                 'tx_laser_disabled_alarm_lanes': item.tx_laser_disabled_alarm_lanes
                                 }
                count += 1
            return output
        except ConnectError as err:
            sys.stdout.write("Error")
            sys.stdout.flush()
            sys.exit(0)