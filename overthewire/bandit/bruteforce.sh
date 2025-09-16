hostname=$1
port=$2
file=$3
lines=$(wc -l $file)
echo $lines



nc $hostname $port | for i in {0..$lines}; do
	read message
	error=$(grep 'Please' $message);
	if [$error == '']; then  
		echo "$message" > ./password_here
		echo " $(read)" > ./password_here
		break
	fi

	line=$(sed -n "$(i)q;d" $file)
	echo "$line"
done

		

