% create TCP socket
raspi = tcpip('10.42.0.249', 5006)

% Matlab will wait maximum of 0.1 sec to receive TCP packet
raspi.timeout = 0.1

% connect to Raspberry
fopen(raspi);

% open fuzzy logic 
fuzzy = readfis('Robot');

while 1
    rawData = fread(obj, 48, 'uchar');
    
    if isempty(rawData)
        %no data was received
    else
        decodedData = jsondecode(transpose(native2unicode(rawData)))

        left = str2num(string(decodedData(1)))
        frontLeft = str2num(string(decodedData(2)))
        front = str2num(string(decodedData(3)))
        frontRight = str2num(string(decodedData(4)))
        right = str2num(string(decodedData(5)))
        
        z = evalfis([left, frontLeft, front, frontRight, right], fuzzy);

        fwrite(obj, jsonencode({w;h}));
    end
end