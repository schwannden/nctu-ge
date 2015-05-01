printf "%-8s%-12s%-12s%-12s%-12s%-12s\n" "major" "tooHigh" "fiveDOK" "moreCredit" "isBad" "isGood"
echo '==================================================================='
sh statistics.sh -m all  >  body
sh statistics.sh -m fl   >> body
sh statistics.sh -m me   >> body
sh statistics.sh -m bio  >> body
sh statistics.sh -m math >> body
sh statistics.sh -m cs   >> body
sh statistics.sh -m ee   >> body
sh statistics.sh -m tlm  >> body
sh statistics.sh -m hs   >> body

echo "all    " >  header
echo "fl     " >> header
echo "me     " >> header
echo "bio    " >> header
echo "math   " >> header
echo "cs     " >> header
echo "ee     " >> header
echo "tlm    " >> header
echo "hs     " >> header
paste header body

printf "%-8s%-12s%-12s%-12s%-12s%-12s\n" "grad" "tooHigh" "fiveDOK" "moreCredit" "isBad" "isGood"
echo '==================================================================='
sh statistics.sh -g 00   >  body
sh statistics.sh -g 01   >> body
sh statistics.sh -g 02   >> body
sh statistics.sh -g 03   >> body
echo "00     " >  header
echo "01     " >> header
echo "02     " >> header
echo "03     " >> header
paste header body

rm header body
