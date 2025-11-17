-- ejercicio 1
SELECT firstname, lastname, country
FROM customers
WHERE country = 'Brazil'

-- ejercicio 2

SELECT lastname, firstname, title
FROM employees
where title = 'Sales Support Agent'

-- ejercicio 3

SELECT name
FROM tracks
where composer = 'AC/DC'

SELECT t.Name, t.Composer, a.Title
from tracks as t
Inner join albums as a
ON t.AlbumId = a.AlbumId
inner join artists as ar
on a.ArtistId = ar.ArtistId where ar.Name = 'AC/DC'

--ejercicio 4

SELECT c.FirstName, c.LastName, c.CustomerId, c.Country 
from customers as c
where country != 'USA'

--ejercicio 5
SELECT firstname ||' ' || lastname as Nombre_Completo, address ||', ' || city ||', ' || state||', ' || country as Direccion, email
from employees
where title = 'Sales Support Agent'

--ejercicio 6
select billingcountry from invoices
group BY billingcountry

--ejercicio 7
SELECT COUNT(customerid) as numero_clientes , state
from customers
where country = 'USA'
group by state

-- ejercicio 8
SELECT sum(quantity) as total_articulos FROM invoice_items
where invoiceid = 37

-- ejercicio 9

SELECT COUNT(t.TrackId) as numero_canciones
from tracks as t
Inner join albums as a
ON t.AlbumId = a.AlbumId
inner join artists as ar
on a.ArtistId = ar.ArtistId where ar.Name = 'AC/DC'

--ejercicio 10
SELECT invoiceid, sum(quantity) as total_articulos FROM invoice_items
GROUP by invoiceid

-- ejercicio 11
SELECT billingcountry, COUNT(invoiceid) as total_facturas FROM invoices
group by billingcountry

-- ejercicio 12
select strftime('%Y', InvoiceDate), count(invoiceid)  from invoices 
GROUP by strftime('%Y', InvoiceDate) having strftime('%Y', InvoiceDate) in ('2009', '2011')


-- ejercicio 13
SELECT COUNT(InvoiceId) AS total_facturas
FROM invoices
WHERE InvoiceDate BETWEEN '2009-01-01' AND  '2011-12-31'

--ejercicio 14

select count(customerid), country 
from customers
where country in ('Spain', 'Brazil')
group by country

--ejercicio 15

select name
from tracks 
where name LIKE ('You%')

--SEGUNDA PARTE

--ejercicio 1
select c.FirstName, c.lastname, i.InvoiceId, i.InvoiceDate, i.BillingCountry
FROM customers AS c
inner join invoices as i
on c.country = i.BillingCountry
where i.BillingCountry = 'Brazil'

--ejercicio 2
SELECT i.InvoiceId, e.EmployeeId, e.FirstName || ' ' || e.LastName AS SalesAgent
FROM invoices i
JOIN customers c ON i.CustomerId = c.CustomerId
JOIN employees e ON c.SupportRepId = e.EmployeeId

--ejercicio 3

SELECT c.FirstName || ' ' || c.LastName AS Customer,c.Country,e.FirstName || ' ' || e.LastName AS SalesAgent,i.Total
FROM invoices AS i
JOIN customers c ON i.CustomerId = c.CustomerId
JOIN employees e ON c.SupportRepId = e.EmployeeId

--ejercicio 4

SELECT ii.InvoiceId, t.Name AS TrackName, ii.UnitPrice, ii.Quantity
FROM invoice_items as ii
JOIN tracks t ON ii.TrackId = t.TrackId

--ejercicio 5
SELECT t.Name AS Nombre, mt.Name AS Formato, a.Title AS Album, g.Name AS Genero
FROM tracks AS t
JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId
JOIN albums a ON t.AlbumId = a.AlbumId
JOIN genres g ON t.GenreId = g.GenreId

--ejercicio 6
select pl.Name, count(plt.TrackId)
from playlists as pl
left join playlist_track as plt
on pl.PlaylistId = plt.PlaylistId
group by pl.PlaylistId

--ejercicio 7

select em.EmployeeId, em.FirstName || ' '|| em.LastName as Agente, sum(i.Total) as Venta_total
from employees as em 
JOIN customers AS c ON em.EmployeeId = c.SupportRepId
JOIN invoices AS i ON c.CustomerId = i.CustomerId
group by em.EmployeeId
order by Venta_total 

--ejercicio 8

select em.EmployeeId, em.FirstName || ' '|| em.LastName as Agente, sum(i.Total) as Venta_total
from employees as em 
JOIN customers AS c ON em.EmployeeId = c.SupportRepId
JOIN invoices AS i ON c.CustomerId = i.CustomerId
WHERE strftime('%Y', i.InvoiceDate) = '2009'
group by em.EmployeeId
order by Venta_total DESC

--ejercicio 9

SELECT ar.Name AS Artista, SUM(ii.UnitPrice * ii.Quantity) AS Ventas
FROM invoice_items AS ii
JOIN tracks AS t ON ii.TrackId = t.TrackId
JOIN albums AS al ON t.AlbumId = al.AlbumId
JOIN artists AS ar ON al.ArtistId = ar.ArtistId
GROUP BY ar.ArtistId
ORDER BY Ventas DESC
LIMIT 3
