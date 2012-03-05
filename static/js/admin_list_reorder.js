django.jQuery(document).ready(function() {
    // Set this to the name of the column holding the position
    pos_field = 'index';
    
    // Determine the column number of the position field
    pos_col = null;
    
    cols = django.jQuery('.changelist-results tbody tr:first').children()
    
    for (i = 0; i < cols.length; i++) {
        inputs = django.jQuery(cols[i]).find('input[name*=' + pos_field + ']')
        
        if (inputs.length > 0) {
            // Found!
            pos_col = i;
            break;
        }
    }
    
    if (pos_col == null) {
        return;
    }
    
    // Some visual enhancements
    header = django.jQuery('.changelist-results thead tr').children()[pos_col]
    django.jQuery(header).css('width', '1em')
    django.jQuery(header).children('a').text('#')
    
    // Hide position field
    django.jQuery('.changelist-results tbody tr').each(function(index) {
        pos_td = django.jQuery(this).children()[pos_col];
        input = django.jQuery(pos_td).children('input').first();
        input.hide();
        
        label = django.jQuery('<strong>' + input.attr('value') + '</strong>');
        django.jQuery(pos_td).append(label);
    });
    
    // Determine sorted column and order
    sorted = django.jQuery('.changelist-results thead th.sorted');
    sorted_col = django.jQuery('.changelist-results thead th').index(sorted);
    sort_order = sorted.hasClass('descending') ? 'desc' : 'asc';
    
    if (sorted_col != pos_col) {
        // Sorted column is not position column, bail out
        console.info("Sorted column is not %s, bailing out", pos_field);
        return;
    }
    
    django.jQuery('.changelist-results tbody tr').css('cursor', 'move');
    
    // Make tbody > tr sortable
    django.jQuery('.changelist-results tbody').sortable({
        axis: 'y',
        items: 'tr',
        cursor: 'move',
        update: function(event, ui) {
            item = ui.item;
            items = django.jQuery(this).find('tr').get();
            
            if (sort_order == 'desc') {
                // Reverse order
                items.reverse();
            }
            
            django.jQuery(items).each(function(index) {
                pos_td = django.jQuery(this).children()[pos_col];
                input = django.jQuery(pos_td).children('input').first();
                label = django.jQuery(pos_td).children('strong').first();
                
                input.attr('value', index);
                label.text(index);
            });
            
            // Update row classes
            django.jQuery(this).find('tr').removeClass('row1').removeClass('row2');
            django.jQuery(this).find('tr:even').addClass('row1');
            django.jQuery(this).find('tr:odd').addClass('row2');
        }
    });
});