# Start a Browser going to localhost:3000
# xdg-open http://localhost:3000

# Reset the "exited_cleanly" flag for chromium
sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' \
    ~/.config/chromium/Default/Preferences

#Launch a Chrome browser in kiosk mode
/usr/lib/chromium-browser/chromium-browser-v7 --force-renderer-accessibility --enable-remote-extensions --enable-pinch --enable-crashpad --start-fullscreen --hide-crash-restore-bubble --kiosk --app=http://localhost:3000