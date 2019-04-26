echo 10.1.23.200
scp -o StrictHostKeyChecking=no $1 root@10.1.23.200:/fw.bin
echo 10.1.23.201
scp -o StrictHostKeyChecking=no $1 root@10.1.23.201:/fw.bin
echo 10.1.23.202
scp -o StrictHostKeyChecking=no $1 root@10.1.23.202:/fw.bin
echo 10.1.23.203
scp -o StrictHostKeyChecking=no $1 root@10.1.23.203:/fw.bin
echo 10.1.23.204
scp -o StrictHostKeyChecking=no $1 root@10.1.23.204:/fw.bin

ssh -o StrictHostKeyChecking=no root@10.1.23.200 'upgrade_tool --debug /fw.bin' > dev1.txt &
ssh -o StrictHostKeyChecking=no root@10.1.23.201 'upgrade_tool --debug /fw.bin' > dev2.txt &
ssh -o StrictHostKeyChecking=no root@10.1.23.202 'upgrade_tool --debug /fw.bin' > dev3.txt &
ssh -o StrictHostKeyChecking=no root@10.1.23.203 'upgrade_tool --debug /fw.bin' > dev4.txt &
ssh -o StrictHostKeyChecking=no root@10.1.23.204 'upgrade_tool --debug /fw.bin' > dev5.txt &

Sleep 100
#echo Device 1 ouptut is $DEV1 `cat dev1.txt`
echo Device 2 ouptut is $DEV2 `cat dev2.txt`
echo Device 3 ouptut is $DEV3 `cat dev3.txt`
echo Device 4 ouptut is $DEV4 `cat dev4.txt`
echo Device 5 ouptut is $DEV5 `cat dev5.txt`

