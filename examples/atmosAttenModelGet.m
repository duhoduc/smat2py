function [atmosAtten] = atmosAttenModelGet()
%% Attenuation because of atmosphere
    atmosAtten{1} = struct('precipitationRate', 3, ...   % [mm/h], precipitationRate
        'clearSky', 0.15, ...                   % [dB/km], Attenuation in clear sky
        'precipitation', 'Rain', ...            % {'None', 'Rain', 'WetSnow','DrySnow'}, Type of precipitation
        'hStart', 0, ...                        % From which height.
        'hEnd', 1000);                          % To which height.
    atmosAtten{end+1} = struct('precipitationRate', 3, ...   % [mm/h], precipitationRate
        'clearSky', 0.15, ...                   % [dB/km], Attenuation in clear sky
        'precipitation', 'WetSnow', ...         % {'None', 'Rain', 'WetSnow','DrySnow'}, Type of precipitation
        'hStart', 1000, ...                     % From which height.
        'hEnd', 2000);                          % To which height.
    atmosAtten{end+1} = struct('precipitationRate', 3, ...   % [mm/h], precipitationRate
        'clearSky', 0.15, ...                   % [dB/km], Attenuation in clear sky
        'precipitation', 'DrySnow', ...         % {'None', 'Rain', 'WetSnow','DrySnow'}, Type of precipitation
        'hStart', 2000, ...                     % From which height.
        'hEnd', 3500);                          % To which height.
    atmosAtten{end+1} = struct('precipitationRate', 3, ...   % [mm/h], precipitationRate
        'clearSky', 0.15, ...                   % [dB/km], Attenuation in clear sky
        'precipitation', 'DrySnow', ...         % {'None', 'Rain', 'WetSnow','DrySnow'}, Type of precipitation
        'hStart', 3500, ...                     % From which height.
        'hEnd', Inf);                          % To which height.
end
