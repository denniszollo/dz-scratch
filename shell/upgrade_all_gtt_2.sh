declare -a arr=("10.1.23.221" 
                "10.1.23.220"
                "10.1.23.231"
                "10.1.23.232"
                )

for i in "${arr[@]}"
do
  echo $i
  ./upgrade_1.sh $1 "$i" &
done

