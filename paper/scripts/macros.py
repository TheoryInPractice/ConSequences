import seaborn as sns

deep_colors = {'freetdi': sns.color_palette('deep')[0],
          'meiji': sns.color_palette('deep')[1],
          'netcon': sns.color_palette('deep')[2],
          'quickbb': sns.color_palette('deep')[5],
          'stoch': sns.color_palette('deep')[3],
          'liquid': sns.color_palette('deep')[4]}

colors = {'freetdi': sns.color_palette("hls", 8)[5],
        'meiji': sns.color_palette("hls", 8)[3],
        'netcon': sns.color_palette("hls", 8)[0],
        'quickbb': sns.color_palette("hls", 8)[1],
        'stoch': sns.color_palette("hls", 8)[6],
        'liquid': sns.color_palette("hls", 8)[7]}

markers = {'freetdi': 'P',
           'meiji': 'o',
           'netcon': 'X'}
