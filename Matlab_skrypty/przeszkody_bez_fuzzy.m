%plik=fopen('wyniki.txt','wt');

obj = tcpip('10.42.0.249', 5006)
obj.timeout = 0.1
fopen(obj);

while 1

incoming = fread(obj, 12, 'uchar');

if isempty(incoming)
%nothing
else
    
data = jsondecode(transpose(native2unicode(incoming)))

left = str2num(string(data(1)))
front = str2num(string(data(2)))
right = str2num(string(data(3)))

%fwrite(obj, jsonencode({40; 40}))

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
w = 40;
h = 40;
end

if (lewa == 0 && srodek == 0 && prawa == 1)
w = -40;
h = 40;
end

if (lewa == 0 && srodek == 1 && prawa == 0)
w = -40;
h = 40;
end

if (lewa == 0 && srodek == 1 && prawa == 1)
w = -40;
h = 40;
end

if (lewa == 1 && srodek == 0 && prawa == 0)
w = 40;
h = -40;
end

if (lewa == 1 && srodek == 0 && prawa == 1)
w = 40;
h = 40;
end

if (lewa == 1 && srodek == 1 && prawa == 0)
w = 40;
h = -40;
end

if (lewa == 1 && srodek == 1 && prawa == 1)
w = -40;
h = 40;
end

fwrite(obj, jsonencode({w;h}));

end
end