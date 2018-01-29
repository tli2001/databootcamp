Sub clearsummaries()
    Dim ws As Worksheet
    
    For Each ws In Worksheets
    ws.Range("J1", "Q1000").Value = ""
    ws.Range("J1", "Q1000").ClearFormats
    Next ws
    
End Sub

Function ispositive(x As Double) As Boolean
    If x < 0 Then
        ispositive = False
    Else: ispositive = True
    End If
End Function

Sub test()
    Dim x As Double
    x = -4
    MsgBox (ispositive(x))
   
End Sub


Sub stockstats()
    'Easy section variables
    Dim ws As Worksheet
    Dim ticker As String
    Dim prevTicker As String
    Dim tickVol As Double
    Dim sumRow As Long
    Dim lastRow As Long 'length of data
    
    'Moderate section variables
    Dim tickOpenPrice As Double
    Dim tickClosePrice As Double
    Dim tickPriceChange As Double ' Close Price - Open Price
    Dim tickPercentChange As Double ' [(Price Change) / Open Price)]
    Dim lastSumRow As Long 'length of summary
    Dim x As Double 'used for checking if positive or negative
         
    'Hard section variables
    Dim greatValues(1 To 3) As Double
    
'****************************************************************************************
'use this section if comparing greatest values across all sheets
'        greatValues(1) = 0 'Set start volume
'        greatValues(2) = 0 'Set start % increase
'        greatValues(3) = 0 'Set start % decrease
'****************************************************************************************
    
    Dim greatTick(1 To 3) As String 'To store ticker names of greatValues array
         
    For Each ws In Worksheets
        tickVol = 0
        sumRow = 2
        lastRow = ws.Cells(Rows.Count, 1).End(xlUp).Row
        'Debug.Print ("lastRow = " + CStr(lastRow))
        'assign first ticker name and first ticker open price
        prevTicker = ws.Cells(2, 1).Value
        tickOpenPrice = ws.Cells(2, 3).Value
        'Debug.Print (ticker & " " & tickOpenPrice)
        
        ws.Range("J1") = "Ticker"
        ws.Range("K1") = "Volume"
        ws.Range("L1") = "Price Change"
        ws.Range("M1") = "Percent Change"

'****************************************************************************************
'use this section if comparing greatest values within each sheet
        greatValues(1) = 0 'Set start volume
        greatValues(2) = 0 'Set start % increase
        greatValues(3) = 0 'Set start % decrease
'****************************************************************************************

        For i = 2 To lastRow + 1 'replace 1000 with lastRow after testing
            ticker = ws.Cells(i, 1).Value

            If ticker = prevTicker Then
                tickVol = tickVol + ws.Cells(i, 7).Value
                'Debug.Print (ws.Cells(i, 7).Value)
                'Debug.Print (tickVol)

            Else
                'Print Ticker and total volume
                ws.Range("J2").Cells(sumRow - 1, 1).Value = prevTicker
                ws.Range("K2").Cells(sumRow - 1, 1).Value = tickVol
                
                'Check if values are greatest Vol
                If tickVol > greatValues(1) Then
                    greatValues(1) = tickVol
                    greatTick(1) = prevTicker
                    End If
                
                'Calculate annual price change and percentage
                tickClosePrice = ws.Cells(i - 1, 6).Value
                tickPriceChange = tickClosePrice - tickOpenPrice
                If tickOpenPrice <> 0 Then
                    tickPercentChange = tickPriceChange / tickOpenPrice
                    Else: tickPercentChange = 0
                    End If
                    
                'Debug.Print ("Close Price = " + CStr(tickClosePrice) + " in Row " & i)
                'Debug.Print ("Open Price = " + CStr(tickOpenPrice))
                'Debug.Print ("% Change = " + CStr(tickPercentChange))
                ws.Range("L2").Cells(sumRow - 1, 1).Value = tickPriceChange
                ws.Range("M2").Cells(sumRow - 1, 1).Value = tickPercentChange
                
                'Check if values are greatest % increase/decrease
                If tickPercentChange > greatValues(2) Then
                    greatValues(2) = tickPercentChange
                    greatTick(2) = prevTicker
                    End If
                If tickPercentChange < greatValues(3) Then
                    greatValues(3) = tickPercentChange
                    greatTick(3) = prevTicker
                    End If
                
                'add 1 to summary table row, then start the new ticker volume
                sumRow = sumRow + 1
                'reset ticker volume to first volume amount of new ticker
                tickVol = ws.Cells(i, 7).Value
                tickOpenPrice = ws.Cells(i, 3).Value
                prevTicker = ticker
            End If
        Next i
        
        lastSumRow = ws.Cells(Rows.Count, "L").End(xlUp).Row
        'Debug.Print ("lastSumRow = " & lastSumRow)
        ws.Range("L2", "L" & lastSumRow).Style = "Currency"
        ws.Range("M2", "M" & lastSumRow).NumberFormat = "0.00%"
        For j = 2 To lastSumRow
            'Debug.Print (ws.Range("L" & j).Value)
            x = ws.Range("L" & j).Value
            If ispositive(x) = True Then
                ws.Cells(j, "L").Interior.Color = vbGreen
            Else
                ws.Cells(j, "L").Interior.Color = vbRed
            End If
        Next j
        
'****************************************************************************************
'use this section if comparing greatest values within each sheet
        ws.Range("O2") = "Greatest Volume"
        ws.Range("O3") = "Greatest % Increase"
        ws.Range("O4") = "Greatest % Decrease"
        ws.Range("O2", "O4").Columns.AutoFit
    
        ws.Range("P1") = "Ticker"
        ws.Range("P2") = greatTick(1)
        ws.Range("P3") = greatTick(2)
        ws.Range("P4") = greatTick(3)
   
        ws.Range("Q1") = "Value"
        ws.Range("Q2") = greatValues(1)
        ws.Range("Q3") = greatValues(2)
        ws.Range("Q3").NumberFormat = "0.00%"
        ws.Range("Q4") = greatValues(3)
        ws.Range("Q4").NumberFormat = "0.00%"
        ws.Range("Q1", "Q4").Columns.AutoFit
'****************************************************************************************

'        Exit For 'used when testing on a single sheet
    Next ws
   
'****************************************************************************************
'use this section if comparing greatest values across all sheets
'        Range("O2") = "Greatest Volume"
'        Range("O3") = "Greatest % Increase"
'        Range("O4") = "Greatest % Decrease"
'        Range("O2", "O4").Columns.AutoFit
'
'        Range("P1") = "Ticker"
'        Range("P2") = greatTick(1)
'        Range("P3") = greatTick(2)
'        Range("P4") = greatTick(3)
'
'        Range("Q1") = "Value"
'        Range("Q2") = greatValues(1)
'        Range("Q3") = greatValues(2)
'        Range("Q3").NumberFormat = "0.00%"
'        Range("Q4") = greatValues(3)
'        Range("Q4").NumberFormat = "0.00%"
'        Range("Q1", "Q4").Columns.AutoFit
'****************************************************************************************


End Sub

