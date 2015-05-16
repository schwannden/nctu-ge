BEGIN {
  tooHigh=0
  fiveDOK=0
  distOK[1]=0
  distOK[2]=0
  distOK[3]=0
  distOK[4]=0
  moreCredit=0
  isBad=0
  isGood=0
}
{
  if ( $2 == 1 ) tooHigh = tooHigh + 1;
  if ( $3 == 1 ) fiveDOK = fiveDOK + 1;
  distOK[$4] = distOK[$3] + 1;
  if ( $5 == 1 ) moreCredit = moreCredit + 1;
  if ( $6 == 1 ) isBad = isBad + 1;
  if ( $7 == 1 ) isGood = isGood + 1;
}
END {
  tooHighRatio = tooHigh / NR * 100;
  fiveDOKRatio = fiveDOK / NR * 100;
  moreCreditRatio = moreCredit / NR * 100;
  isBadRatio = isBad / NR * 100;
  isGoodRatio = isGood / NR * 100;
  printf "%-12s%-12s%-12s%-12s%-12s%s\n", tooHighRatio, fiveDOKRatio, moreCreditRatio, isBadRatio, isGoodRatio, NR
}
