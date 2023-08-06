import re

from cvr_osc_lib import AvatarParameterChange, OscInterface


def avatar_parameter_change(data: AvatarParameterChange):
    print(f'The parameter {data.parameter_name} has changed to the value: {data.parameter_value}')


if __name__ == '__main__':
    osc = OscInterface()

    # Initialize the functions to react on events (needs to be set before starting the interface)

    # Listen to avatar parameter changes
    #osc.on_avatar_parameter_changed(avatar_parameter_change)
    # osc.on_avatar_parameter_changed_legacy(avatar_parameter_change)
    #osc.on_avatar_parameter_changed_legacy(lambda x: x)
    #osc.on_tracking_device_data_updated(lambda x: x)
    #osc.on_tracking_play_space_data_updated(lambda x: x)

    # Start the osc interface (starts both osc sender client and listener server)
    # You can optionally not start the sender (it will be started if you attempt to send an osc msg)
    # You only need to call the start if you intend to listen to osc messages, otherwise you don't need to which will
    # keep the 9001 port free for other osc apps :) You can have multiple senders, but only 1 server bound to a port
    osc.start(start_sender=True, start_receiver=False)

    # Inform the mod that a new osc server is listening, so it resends all the cached state (if previously connected)
    # osc.send_config_reset()
    osc.send_avatar_parameter_legacy(AvatarParameterChange('K_Outfit', True))

    # handlers_for_address('/avatar/parameters/TailCtl')

    #input()
