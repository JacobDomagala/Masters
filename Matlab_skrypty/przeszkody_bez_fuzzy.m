plik=fopen('wyniki.txt','wt');
while 1
y = fread(lewa_cz,4);
%pause(0.2);
x = fread(srod_cz,4);
%pause(0.2);
g = fread(prawy_cz,4);
%pause(0.2);
left = str2double(string(transpose(y)));
front = str2double(string(transpose(x)));
right = str2double(string(transpose(g)));


parametr1_lewa = (left - 1)/(2-1);
parametr2_lewa = (40 - left)/(40-2);
wynik_lewa_sm = min(parametr1_lewa,parametr2_lewa);
parametr3_lewa = (left - 2)/(40-2);
parametr4_lewa = (41 - left)/(41-40);
wynik_lewa_big = min(parametr3_lewa,parametr4_lewa);
if wynik_lewa_sm < wynik_lewa_big 
    lewa = 0;
else lewa = 1;
end

parametr1_srodek = (front - 1)/(2-1);
parametr2_srodek = (40 - front)/(40-2);
wynik_srodek_sm = min(parametr1_srodek,parametr2_srodek);
parametr3_srodek = (front - 2)/(40-2);
parametr4_srodek = (41 - front)/(41-40);
wynik_srodek_big = min(parametr3_srodek,parametr4_srodek);
if wynik_srodek_sm < wynik_srodek_big 
    srodek = 0;
else srodek = 1;
end

parametr1_prawa = (right - 1)/(2-1);
parametr2_prawa = (40 - right)/(40-2);
wynik_prawa_sm = min(parametr1_prawa,parametr2_prawa);
parametr3_prawa = (right - 2)/(40-2);
parametr4_prawa = (41 - right)/(41-40);
wynik_prawa_big = min(parametr3_prawa,parametr4_prawa);
if wynik_prawa_sm < wynik_prawa_big 
    prawa = 0;
else prawa = 1;
end

if ((lewa == 0) && (srodek == 0) && (prawa == 0))
w = '40';
h = '40';
end

if (lewa == 0 && srodek == 0 && prawa == 1)
w = '-40';
h = '40';
end

if (lewa == 0 && srodek == 1 && prawa == 0)
w = '-40';
h = '40';
end

if (lewa == 0 && srodek == 1 && prawa == 1)
w = '-40';
h = '40';
end

if (lewa == 1 && srodek == 0 && prawa == 0)
w = '40';
h = '-40';
end

if (lewa == 1 && srodek == 0 && prawa == 1)
w = '40';
h = '40';
end

if (lewa == 1 && srodek == 1 && prawa == 0)
w = '40';
h = '-40';
end

if (lewa == 1 && srodek == 1 && prawa == 1)
w = '-40';
h = '40';
end

%L = num2str(w);
%P = num2str(h);
%pause(0.1);
format = 'lewa: %2.2f, srodek: %2.2f, prawa: %2.2f lewe kolo: %s prawe kolo: %s \n';
fprintf(plik, format,left,front,right,w,h);
fwrite(pred,w);
pause(0.3);
fwrite(pred,h);
%pause(0.1);
end