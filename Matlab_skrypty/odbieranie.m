plik=fopen('dane_z_cz.txt','wt');
while (1)
y = fread(lewa_cz,4);
x = fread(srod_cz,4);
g = fread(prawy_cz,4);
left = str2double(string(transpose(y)))
front = str2double(string(transpose(x)))
right = str2double(string(transpose(g)))
format = 'lewa: %2.2f, srodek: %2.2f, prawa: %2.2f \n';
fprintf(plik, format,left,front,right);
end
