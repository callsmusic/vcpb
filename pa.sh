pacmd load-module module-null-sink sink_name=MySink
pactl load-module module-remap-source master=MySink.monitor source_name=virtual_microphone source_properties=device.description=VoiceChatPyroBot
