<!DOCTYPE html>
<html><head>
<link type="text/css" href="style.css" rel="stylesheet"></link>
<style>
body {
  font-family:Arial, Helvetica, sans-serif;
  font-size:12px;
}

span {
  font-weight:700;
  text-transform: uppercase;
}

.datagrid table {
border-collapse:collapse;
text-align:left;
width:100%;
}

.datagrid {
background:#fff;
overflow:hidden;
border:1px solid #8C8C8C;
}

.datagrid table td,.datagrid table th {
padding:14px;
}

.datagrid table thead th {
background:0;
filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#8C8C8C',endColorstr='#7D7D7D');
background-color:#8C8C8C;
color:#FFF;
  font-weight:700;
border-left:1px solid #A3A3A3;
}

.datagrid table thead th:first-child {
border:none;
}

.datagrid table tbody td {
border-left:1px solid #DBDBDB;
font-weight:400;
}

.datagrid tr:nth-child(even) {background: #EBEBEB}
.datagrid tr:nth-child(odd) {background: #FFF}

.datagrid table tbody td:first-child {
border-left:none;
}

.datagrid table tbody tr:last-child td {
border-bottom:none;
}
</style>
</head>

<body>
%for user in objects:
  %for medic in get_medics(user):
  <div>
    <br/>
    <p><span>${_("FECHA")}: </span>${formatLang(get_date(date), date=True)}</p>
    <p><span>${_("MEDICO")}: </span>${user.name}</p>
    <br/>
  </div>
  <div class="datagrid">
    <table>
      <thead>
        <tr>
          <th style="width: 80px;"><center>${_("HORA")}</center></th>
          <th style="width: 170px;">${_("PACIENTE")}</th>
          <th>${_("OBSERVACIONES")}</th>
        </tr>
      </thead>
      <tbody>
        %for meeting in get_meetings(user.id, get_date(date)):
        <tr>
          <td><center>${format_date(date_locale(meeting.start), "%H:%M")} - ${format_date(date_locale(meeting.stop), "%H:%M")}</center></td>
          <td>${meeting.patient_id.name}</td>
          <td>${meeting.description or ""}</td>
        </tr>
         %endfor
      </tbody>
    </table>
  </div>
  %endfor
  <p style="page-break-before: always"></p>
%endfor    
</body>

</html>