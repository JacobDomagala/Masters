plik=fopen('dane_z_cz_przerwy.txt','wt');
format = 'lewe kolo: %s prawe kolo: %s \n';
while(1)
w = '40';
h = '40';
fwrite(pred,w);
fwrite(pred,h);
fprintf(plik, format,w,h);
pause(1);
w='0';
h='0';
fwrite(pred,w);
fwrite(pred,h);
pause(1);
fprintf(plik, format,w,h);
end;