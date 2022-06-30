from upytl import html as h

# flake8: noqa E226

upytl_demo = {
    h.Html():{
        h.Head():{
            h.Title():"[[app_get('app_name')]]",
                h.Meta(charset='utf-8'):'',
            },
            h.Body():{
                h.Div():'[[msg]]'
        }
    }
}
