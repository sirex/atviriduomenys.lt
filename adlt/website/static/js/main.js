require(['require'], function(require) {

    $('input.typeahead').each(function () {
        var $this = $(this);

        var source = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('title'),
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            prefetch: {
                cache: false,
                url: 'http://127.0.0.1:8000' + $this.data('source')
            }
        });

        $this.typeahead({hint: true, highlight: true, minLength: 1}, {
            name: $this.attr('name'),
            display: 'title',
            source: source
        });

        $this.bind('typeahead:change', function(ev, value) {
            if ($this.data('selected') != value) {
                $('#' + $this.data('input')).val(value);
            }
        });

        $this.bind('typeahead:select', function(ev, value) {
            $('#' + $this.data('input')).val(value.pk);
            $this.data('selected', value.title);
        });

    });

});
