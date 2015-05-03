require(['require'], function(require) {

    $('input.typeahead').each(function () {
        var $this = $(this);
        var source = new Bloodhound({
            initialize: false,
            // identify: function(obj) { return obj.title; },
            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('title'),
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            // local: [
            //     {title: 'vienas', pk: 1},
            //     {title: 'du',     pk: 2},
            //     {title: 'trys',   pk: 3},
            //     {title: 'keturi', pk: 4},
            //     {title: 'penki',  pk: 5}
            // ]
            prefetch: 'http://127.0.0.1:8000' + $this.data('source')
        });

        console.log('http://127.0.0.1:8000' + $this.data('source'));

        function sync(datums) {
            console.log('datums from `local`, `prefetch`, and `#add`');
            console.log(datums);
        }

        var promise = source.initialize();
        promise.done(function() {
            console.log('ready to go');
            source.search('ma', sync);
        }).fail(function() {
            console.log('failed');
        });

        // function search(q, cb) {
        //     console.log(q);
        //     cb(['vienas', 'du', 'trys']);
        // }

        var options = {
            hint: true,
            highlight: true,
            minLength: 1
        };
        $this.typeahead(options, {
            name: $this.attr('name'),
            display: 'title',
            source: source
        });

        $this.bind('typeahead:change', function(ev, value) {
            console.log('typeahead:change');
            console.log(value);
            if ($this.data('selected') != value) {
                $('#' + $this.data('input')).val(value);
            }
        });

        $this.bind('typeahead:select', function(ev, value) {
            console.log('typeahead:select');
            console.log(value);
            $('#' + $this.data('input')).val(value.pk);
            $this.data('selected', value.title);
        });

    });

});
