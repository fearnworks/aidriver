# Compile requirements/requirements for ai_driver
cd ./ai_driver
pip-compile requirements/requirements.in --upgrade
pip-compile requirements/requirements-server.in --upgrade
pip-compile requirements/requirements-dev.in --upgrade
pip-compile requirements/requirements-test.in --upgrade
pip-compile requirements/requirements-ui.in --upgrade
echo "Pin update complete."
cd ..
