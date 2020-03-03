var styles = ['standard', 'dark', 'grid', 'small', 'fancy', 'minimal']

var app = new Vue({
    el: '#books'
    , data: {
        items: []
    }
    , mounted(){
        $.get('jsons/output.json', this.loadInfo.bind(this))
    }
    , methods: {
        loadInfo(data) {
            this.items = data
        }
    }
})

var actions = new Vue({
    el: '#actions'
    , data: {
        items: styles
        , selected: ['standard', 'dark']
    }
    , mounted(){
        this.select()
    }
    , methods: {
        select(ev) {
            $('body')
               .removeClass(this.items.join(' '))
               .addClass(this.selected.join(' '))
        }
    }
})
