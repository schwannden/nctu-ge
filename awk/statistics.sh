#!/bin/bash

########################################
# define help message                  #
########################################
thisFile=`basename $0`
read -d '' help <<- EOF
Usage: ./$thisFile
options:
  -m [all | fl | me | bio | math | cs | ee | tlm | hs ]
  -g [all | 00|01|02|03|99|98|97]
  -h display this message
EOF

########################################
# Set default values                   #
########################################
gradYr=all
major=all
header=false
flID='19'
meID='11'
bioID='17'
mathID='12'
csID='16'
eeID='10'
tlmID='13'
hsID='15'

########################################
# get options                          #
########################################
function getOptions
{
  if [ $# -eq 0 ]
  then
    major=each
    grad=all
  fi
  
  while getopts ":m:g:lh" opt
  do
    case $opt in
      m)
        major=$OPTARG
        ;;
      g)
        gradYr=$OPTARG
        ;;
      l)
        header=true
        ;;
      h)
        echo "$help"
        ;;
      :)
        echo "option -$OPTARG requires an argument"
        echo "$help"
        exit
        ;;
      \?)
        echo un-recognized option
        echo "$help"
        exit
        ;;
    esac
  done
}

function selectGrad
{
  if [ $gradYr == all ]
  then
    awk -f statistics.awk $1
  else
    grep g$gradYr $1 > g$gradYr
    awk -f statistics.awk g$gradYr
    rm g$gradYr
  fi
}

function selectMajor
{
  if [ $major == all ]
  then
    selectGrad "$1"
  else
    grep m$major $1 > m$major
    selectGrad "m$major"
    rm m$major
  fi
}

getOptions "$@"

case $major in
  'all')
    major='all'
    ;;
  'fl')
    major=$flID
    ;;
  'me')
    major=$meID
    ;;
  'bio')
    major=$bioID
    ;;
  'math')
    major=$mathID
    ;;
  'cs')
    major=$csID
    ;;
  'ee')
    major=$eeID
    ;;
  'tlm')
    major=$tlmID
    ;;
  'hs')
    major=$hsID
    ;;
esac

if [ $header == true ]
then
  printf "%-12s%-12s%-12s%-12s%-12s\n" "tooHigh" "fiveDOK" "moreCredit" "isBad" "isGood"
  echo '=================================================================='
fi

selectMajor 2015raw

