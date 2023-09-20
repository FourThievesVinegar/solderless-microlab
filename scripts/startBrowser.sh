# Start a Browser going to localhost:3000
# xdg-open http://localhost:3000

# Hacky suppression of "restore tabs" popover
/usr/lib/chromium-browser/chromium-browser-v7 --no-startup-window --kiosk
# The actual window we want
/usr/lib/chromium-browser/chromium-browser-v7 --force-renderer-accessibility --enable-remote-extensions --enable-pinch --enable-crashpad --start-fullscreen --hide-crash-restore-bubble --kiosk --app=http://localhost:3000