password=$1

for i in {0..9}; do
	for j in {0..9}; do
		for k in {0..9}; do
			for l in {0..9}; do
				echo "$password $i$j$k$l" >> ./pincodes
			done
		done
	done
done

