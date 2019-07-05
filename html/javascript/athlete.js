function checkFileType(name) {
  var ext = name.value.match(/\.([^\.]+)$/)[1];
  switch (ext) {
    case 'pdf':
      break;
    default:
      alert('The FirmU only allows the upload of PDF files, please convert your document to PDF.');
      name.value = '';
  }
}