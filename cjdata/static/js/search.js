var lastSearch = null;

jQuery(document).ready(function($) {
    function split( val ) {
        return val.split( /,\s*/ );
    }
    function extractLast( term ) {
        return split( term ).pop();
    }
    var input_id = "input.autocomplete";
    $(input_id).on('input', function(event) {
        if ( event.keyCode === $.ui.keyCode.TAB && $( this ).autocomplete( "instance" ).menu.active ) {
            event.preventDefault();
        }
    }).autocomplete({
        minLength: 3,
        source: function(request, response) {
            var lastTerm = extractLast(request.term);
            // console.log("request.term: " + lastTerm);
            $.getJSON(searchURL, {
                q: extractLast(request.term)
            })
            .done(function(json) {
                var results = [];
                if (json.results) {
                    results = $.map(json.results, function(val, i) {
                        return val.value;
                    });
                } else {
                    console.log('Error fetching/parsing autocomplete results');
                }
                response(results);
            });
        },
        select: function( event, ui ) {
            var terms = split( this.value );
            // remove the current input
            terms.pop();
            // add the selected item
            terms.push( ui.item.value );
            // add placeholder to get the comma-and-space at the end
            terms.push( "" );
            this.value = terms.join( ", " );
            return false;
        },
        focus: function() {
            // prevent value inserted on focus
            return false;
        }
    });
});
