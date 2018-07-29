echoudp('on',4012);

lewa_cz = udp('10.10.20.40', 4012, 'LocalPort', 3533);
srod_cz = udp('10.10.20.40', 4012, 'LocalPort', 3534);
prawy_cz = udp('10.10.20.40', 4012, 'LocalPort', 3535);

fopen(lewa_cz);
fopen(srod_cz);
fopen(prawy_cz);

pred = udp('10.10.20.40', 4012, 'LocalPort', 3536);
fopen(pred);