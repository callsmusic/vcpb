if [ "$EUID" -eq 0 ]
  then echo "Don't run anything as root!"
  exit
fi
pacmd load-module module-null-sink sink_name=MySink
echo "Loaded successfully."
