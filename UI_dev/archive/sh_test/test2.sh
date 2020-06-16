#!/bin/sh

# ANSWER=`yad --entry --expander="click here to show entry"`
# echo $ANSWER

# if [ $ANSWER == 'y' ]
# then
#    bash test.sh
# else
#    echo "a is not equal to b"
# fi





# values=( $(yad --form --center --width=300 --title="Test" --separator=' ' \
#         --button=Skip:1 \
#         --button=Apply:0 \
#         --field="Radius":NUM \
#             '0!0..30!1!0' \
#         --field="Amount":NUM \
#             '0!0..5!0.01!2') )

values=($(yad --form --columns=2 --title="Test" --separator=' '\
		--field="Firstname:" "Billy" \
		--field="Age:" "21" \
		--field="Lastname:" "Bloggs" \
		--field="Sex::"CB "Male!Female" \
	))

echo ${values[0]}
echo ${values[1]}
echo ${values[2]}
echo ${values[3]}