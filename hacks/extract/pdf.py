def convert():
    import convertapi

    convertapi.api_secret = 'Yg8lKOH0wLJn8OeI'
    result = convertapi.convert('pdf', { 'File': fileinputpath })

    # save to file
    result.file.save(fileoutputpath)

