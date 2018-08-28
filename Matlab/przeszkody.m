% create TCP socket
raspi = tcpip('10.42.0.249', 5006)

% Matlab will wait maximum of 0.05 sec to receive TCP packet
raspi.timeout = 0.05

% connect to Raspberry
fopen(raspi);

% open fuzzy logic 
fuzzy = readfis('przeszkody');

while 1
    rawData = fread(raspi, 12, 'uchar');
    
    if isempty(rawData)
        %no data was received
    else
        decodedData = jsondecode(transpose(native2unicode(rawData)))

        left = str2num(string(decodedData(1)))
        front = str2num(string(decodedData(2)))
        right = str2num(string(decodedData(3)))
        
        result = evalfis([left, front, right], fuzzy);

        leftWheel = fix(result(1))
        rightWheel = fix(result(2))
        
        if leftWheel > 0 && leftWheel < 40
            leftWheel = 50
        elseif leftWheel < 0 && leftWheel > -40
            leftWheel = -50
        end
        
        if rightWheel > 0 && rightWheel < 40
            rightWheel = 50
        elseif rightWheel < 0 && rightWheel > -40
            rightWheel = -50
        end
%         leftWheel = result(1)
%         rightWheel = result(2)
        
%         if (result(1) > 0) && (result(2) > 0)
%             leftWheel = 40;
%             rightWheel = 40;
%         end
%         
%         if (result(1) < result(2)) 
%             leftWheel = -40;
%             rightWheel = 40;
%         end
%         
%         if(result(1) > result(2))
%             leftWheel = 40;
%             rightWheel = -40;
%         end
        
        fwrite(raspi, jsonencode({leftWheel;rightWheel}));
    end
end