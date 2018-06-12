$( document ).ready(function() {
    // First, obtain the text area that is "native" to the page and hide it
    var content_textarea = $('#id__content');
    content_textarea.hide();

    // Insert an editor div after it
    content_textarea.after('<div id="editor"></div>');

    // Set the editor up
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/github");
    editor.getSession().setMode("ace/mode/javascript");

    // Set the contents of the text editor to the same as the text area
    // then update the text area each time something changes in the editor
    editor.getSession().setValue(content_textarea.val());
    editor.getSession().on('change', function(){
        content_textarea.val(editor.getSession().getValue());
    });
    editor.setOptions({
        highlightActiveLine: true,
        highlightSelectedWord: true,
        vScrollBarAlwaysVisible: true,
        highlightGutterLine: true,
        showInvisibles: true,
        showPrintMargin: true,
        showGutter: true,
        displayIndentGuides: true,
        fontSize: "1.2em",
        tabSize: 4,
        enableMultiSelect: true
    });
});
