declare -a arr=("10.1.23.200" 
                "10.1.23.201"
                "10.1.23.202"
                "10.1.23.203"
                "10.1.23.204"
                )

for i in "${arr[@]}"
do
  echo $i
  ./upgrade_1.sh $1 "$i" &
done

