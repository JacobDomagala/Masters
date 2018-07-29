K=readfis('robot');
while 1
y = fread(lewa_cz,6);
x = fread(srod_cz,6);
g = fread(prawy_cz,6);
left = str2num(string(transpose(y)));
front = str2num(string(transpose(x)));
right = str2num(string(transpose(g)));
z = evalfis([left, front, right], K);

if (z(1) > 0) && (z(2) > 0)
     w = '30';
     h = '30';
end

if (z(1) < z(2)) 
     w = '-30';
     h = '30';
end

if (z(1) > z(2))
     w = '30';
     h = '-30';
end

%L = num2str(w);
%P = num2str(h);
fwrite(pred,w);
fwrite(pred,h);
end