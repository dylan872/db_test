# If you want to get your ms acces sql code 
# click Alt+f11 to open a page
# on the page look for insert tab and selct module then paste this code in it
Sub ExportSchemaToSQL()
    Dim db As DAO.Database
    Dim tdf As DAO.TableDef
    Dim fld As DAO.Field
    Dim fileNum As Integer
    Dim sqlString As String
    Dim dataType As String
    
    Set db = CurrentDb
    fileNum = FreeFile
    
    ' Output file path
    Open "C:\Users\Public\AccessSchema.sql" For Output As #fileNum
    
    For Each tdf In db.TableDefs
        ' Ignore hidden and system tables
        If Left(tdf.Name, 4) <> "MSys" And Left(tdf.Name, 1) <> "~" Then
            
            sqlString = "CREATE TABLE " & tdf.Name & " (" & vbCrLf
            
            For Each fld In tdf.Fields
                ' Translate Access data types to SQL standard types
                Select Case fld.Type
                    Case dbBoolean:    dataType = "BOOLEAN"
                    Case dbByte:       dataType = "TINYINT"
                    Case dbInteger:    dataType = "SMALLINT"
                    Case dbLong:       dataType = "INT"
                    Case dbCurrency:   dataType = "DECIMAL(19,4)"
                    Case dbSingle:     dataType = "FLOAT"
                    Case dbDouble:     dataType = "DOUBLE"
                    Case dbDate:       dataType = "DATETIME"
                    Case dbText:       dataType = "VARCHAR(" & fld.Size & ")"
                    Case dbLongBinary: dataType = "BLOB"
                    Case dbMemo:       dataType = "TEXT"
                    Case Else:         dataType = "VARCHAR(255)"
                End Select
                
                sqlString = sqlString & "    " & fld.Name & " " & dataType & "," & vbCrLf
            Next fld
            
            ' Strip the trailing comma and close the CREATE TABLE statement
            sqlString = Left(sqlString, Len(sqlString) - 3) & vbCrLf & ");" & vbCrLf
            
            ' Write to file
            Print #fileNum, sqlString
        End If
    Next tdf
    
    Close #fileNum
    MsgBox "SQL Schema exported to C:\Users\Public\AccessSchema.sql", vbInformation
End Sub