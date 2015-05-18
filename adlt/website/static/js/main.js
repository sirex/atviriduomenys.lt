require(['require'], function(require) {

    $('input.typeahead').each(function () {
        var $this = $(this);

        var source = new Bloodhound({
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('title'),
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            prefetch: {
                cache: false,
                url: 'http://ad.sirex.lt' + $this.data('source')
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

    $('.like-button[data-action]').click(function () {
        var $this = $(this);
        var action_url = $this.data('action');
        var next_label = $this.data('label');

        function update_total_likes(value) {
            var $elem = $this.parents('.input-group').first().find('.total-likes');
            var likes = parseInt($elem.text());
            $elem.text(likes + value);
        }

        $.getJSON(action_url, function(data) {
            if ($this.data('likes')) {
                $this.find('.like').show();
                $this.find('.unlike').hide();
                $this.data('likes', false);
                update_total_likes(-1);
            }
            else {
                $this.find('.like').hide();
                $this.find('.unlike').show();
                $this.data('likes', true);
                update_total_likes(1);
            }
        });
    });

});
