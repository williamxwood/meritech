select 
    case 
        when grades.grade > 7 then students.name
        else null 
        end as names,
    grades.grade, 
    students.marks 
from 
    students
        left join grades 
            on students.marks between grades.min_mark and grades.max_mark
order by 
    grades.grade desc, 
    names asc, 
    students.marks asc;