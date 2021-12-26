"""
These are custom table views to use in conjunction with PyEZ to filter out the information i needed
for daily reports.

These are currently based on RPC calls.
if you need to see which rpc call is used for each command, postend a command with a "| display xml rpc"

"""

"""
BEGINNING OF YML VARIABLES
"""

returnChassisFPCList = """
---
returnChassisFPCList:
    rpc: get-chassis-inventory
    item: .//name[starts-with(.,'FPC')]/parent::*
    key: name
    view: _chassis_fpc_view

_chassis_fpc_view:
    fields:
        fpc: name
        description: description

"""

returnChassisFPCPICList = """
---
returnChassisFPCPICList:
    rpc: get-chassis-inventory
    item: .//name[starts-with(.,'{}')]/parent::*
    key: name
    view: _chassis_fpc_pic_view

_chassis_fpc_pic_view:
    fields:
        fpc: name
        pic: .//chassis-sub-module/name[starts-with(.,'PIC')] | .//chassis-sub-sub-module/name[starts-with(.,'PIC')]
"""


FPCChassisSubModulesPICInformationDetail = """
---
FPCChassisSubModulesPICInformationDetail:
    rpc: get-pic-detail
    item: .//pic-detail/parent::*
    key: pic-detail/port-information/port/port-number
    args:
        fpc-slot: '{}'
        pic-slot: '{}'
    view: _pic_detail_view

_pic_detail_view:
    fields:
        slot: .//pic-detail/slot
        pic_slot: .//pic-detail/pic-slot
        port_number: .//pic-detail/port-information/port/port-number
        cable_type: .//pic-detail/port-information/port/cable-type
        fiber_mode: .//pic-detail/port-information/port/fiber-mode
        wavelength: .//pic-detail/port-information/port/wavelength

"""


interfaceDiagnosticsOptics = """
---
interfaceDiagnosticsOptics:
    rpc: get-interface-optics-diagnostics-information
    item: .//physical-interface/optics-diagnostics/parent::*
    key: .//physical-interface/name
    view: _interface_diagnostics_view

_interface_diagnostics_view:
    fields:
        name: name[starts-with(.,'xe') or starts-with(.,'ge') or starts-with(.,'et')]
        laser_output_power_dbm: .//optics-diagnostics/laser-output-power-dbm
        rx_signal_avg_optical_power_dbm: .//optics-diagnostics/rx-signal-avg-optical-power-dbm | .//optics-diagnostics/laser-rx-optical-power-dbm
        laser_bias_current_high_alarm: .//optics-diagnostics/laser-bias-current-high-alarm
        laser_bias_current_low_alarm: .//optics-diagnostics/laser-bias-current-low-alarm
        laser_bias_current_high_warn: .//optics-diagnostics/laser-bias-current-high-warn
        laser_bias_current_low_warn: .//optics-diagnostics/laser-bias-current-low-warn
        laser_tx_power_high_alarm: .//optics-diagnostics/laser-tx-power-high-alarm
        laser_tx_power_low_alarm: .//optics-diagnostics/laser-tx-power-low-alarm
        laser_tx_power_high_warn: .//optics-diagnostics/laser-tx-power-high-warn
        laser_tx_power_low_warn: .//optics-diagnostics/laser-tx-power-low-warn
        module_temperature_high_alarm: .//optics-diagnostics/module-temperature-high-alarm
        module_temperature_high_warn: .//optics-diagnostics/module-temperature-high-warn
        module_temperature_low_warn: .//optics-diagnostics/module-temperature-low-warn
        module_voltage_high_alarm: .//optics-diagnostics/module-voltage-high-alarm
        module_voltage_low_alarm: .//optics-diagnostics/module-voltage-low-alarm
        module_voltage_high_warn: .//optics-diagnostics/module-voltage-high-warn
        module_voltage_low_warn: .//optics-diagnostics/module-voltage-low-warn
        laser_rx_power_high_alarm: .//optics-diagnostics/laser-rx-power-high-alarm
        laser_rx_power_low_alarm: .//optics-diagnostics/laser-rx-power-low-alarm
        laser_rx_power_high_warn: .//optics-diagnostics/laser-rx-power-high-warn
        laser_rx_power_low_warn: .//optics-diagnostics/laser-rx-power-low-warn
        lane_index: .//optics-diagnostics/optics-diagnostics-lane-values/lane-index
        laser_output_power_dbm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-output-power-dbm
        laser_rx_optical_power_dbm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-optical-power-dbm
        laser_bias_current_high_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-bias-current-high-alarm
        laser_bias_current_low_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-bias-current-low-alarm
        laser_bias_current_high_warn_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-bias-current-high-warn
        laser_bias_current_low_warn_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-bias-current-low-warn
        laser_rx_power_high_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-power-high-alarm
        laser_rx_power_low_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-power-low-alarm
        laser_rx_power_high_warn_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-power-high-warn
        laser_rx_power_low_warn_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/laser-rx-power-low-warn
        tx_loss_of_signal_functionality_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/tx-loss-of-signal-functionality-alarm
        rx_loss_of_signal_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/rx-loss-of-signal-alarm
        tx_laser_disabled_alarm_lanes: .//optics-diagnostics/optics-diagnostics-lane-values/tx-laser-disabled-alarm

"""




"""
END OF YML VARIABLES
"""
