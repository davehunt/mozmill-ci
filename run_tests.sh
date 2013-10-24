echo "Checking patches"
./check_patches.sh || exit $?

echo "Running setup"
./setup.sh

echo "Starting Jenkins"
./start.sh > jenkins.out &
sleep 60

python save_config.py

git --no-pager diff --exit-code
