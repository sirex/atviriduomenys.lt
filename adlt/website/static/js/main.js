require(['require'], function(require) {

    $('input.typeahead').each(function () {
        $this = $(this);
        $this.typeahead(null, {
            name: $this.attr('name'),
            source: new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.whitespace,
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                prefetch: $this.data('source')
            })
        });
    });

});
