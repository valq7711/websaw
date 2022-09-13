from upytl import html as h

# flake8: noqa E226

upytl_demo = {
    h.Html():{
        h.Head():{
            h.Title():"[[app_get('app_name')]]",
                h.Meta(charset='utf-8'):'',
                h.Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.1/css/bulma.min.css'):None, 
            },
            h.Body():{
                h.Div(Class='title'):'[[msg]]',
            h.Footer():{
                h.Div(): 'This is the footer',
            }

        }
    }
}
