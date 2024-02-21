"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import random
import config as cf
from DISClib.ADT import list as lt
# from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
assert cf

"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores
y otra para géneros
"""

# Construccion de modelos


def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {"books": None,
               "authors": None,
               "tags": None,
               "book_tags": None}

    catalog["books"] = lt.newList("ARRAY_LIST",
                                  cmpfunction=comparebooks)
    catalog["authors"] = lt.newList("SINGLE_LINKED",
                                    cmpfunction=compareauthors)
    catalog["tags"] = lt.newList("SINGLE_LINKED",
                                 cmpfunction=comparetagnames)
    catalog["book_tags"] = lt.newList("ARRAY_LIST")

    return catalog


# Funciones para agregar informacion al catalogo

def addBook(catalog, book):
    # Se adiciona el libro a la lista de libros
    lt.addLast(catalog["books"], book)
    # Se obtienen los autores del libro
    authors = book["authors"].split(",")
    # Cada autor, se crea en la lista de libros del catalogo, y se
    # crea un libro en la lista de dicho autor (apuntador al libro)
    for author in authors:
        addBookAuthor(catalog, author.strip(), book)
    return catalog


def addBookAuthor(catalog, authorname, book):
    """
    Adiciona un autor a lista de autores, la cual guarda referencias
    a los libros de dicho autor
    """
    authors = catalog["authors"]
    posauthor = lt.isPresent(authors, authorname)
    if posauthor > 0:
        author = lt.getElement(authors, posauthor)
    else:
        author = newAuthor(authorname)
        lt.addLast(authors, author)
    lt.addLast(author["books"], book)
    return catalog


def addTag(catalog, tag):
    """
    Adiciona un tag a la lista de tags
    """
    t = newTag(tag["tag_name"], tag["tag_id"])
    lt.addLast(catalog["tags"], t)
    return catalog


def addBookTag(catalog, booktag):
    """
    Adiciona un tag a la lista de tags
    """
    t = newBookTag(booktag["tag_id"], booktag["goodreads_book_id"])
    lt.addLast(catalog["book_tags"], t)
    return catalog


# Funciones para creacion de datos

def newAuthor(name):
    """
    Crea una nueva estructura para modelar los libros de
    un autor y su promedio de ratings
    """
    author = {"name": "", "books": None,  "average_rating": 0}
    author["name"] = name
    author["books"] = lt.newList("ARRAY_LIST")
    return author


def newTag(name, id):
    """
    Esta estructura almancena los tags utilizados para marcar libros.
    """
    tag = {"name": "", "tag_id": ""}
    tag["name"] = name
    tag["tag_id"] = id
    return tag


def newBookTag(tag_id, book_id):
    """
    Esta estructura crea una relación entre un tag y
    los libros que han sido marcados con dicho tag.
    """
    booktag = {"tag_id": tag_id, "book_id": book_id}
    return booktag


# Funciones de consulta

def getBooksByAuthor(catalog, authorname):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    posauthor = lt.isPresent(catalog["authors"], authorname)
    if posauthor > 0:
        author = lt.getElement(catalog["authors"], posauthor)
        return author
    return None


def getBestBooks(catalog, number):
    """
    Retorna los mejores libros
    """
    books = catalog["books"]
    bestbooks = lt.newList()
    for cont in range(1, number+1):
        book = lt.getElement(books, cont)
        lt.addLast(bestbooks, book)
    return bestbooks


def countBooksByTag(catalog, tag):
    """
    Retorna los libros que fueron etiquetados con el tag
    """
    tags = catalog["tags"]
    bookcount = 0
    pos = lt.isPresent(tags, tag)
    if pos > 0:
        tag_element = lt.getElement(tags, pos)
        if tag_element is not None:
            for book_tag in lt.iterator(catalog["book_tags"]):
                if tag_element["tag_id"] == book_tag["tag_id"]:
                    bookcount += 1
    return bookcount


def bookSize(catalog):
    return lt.size(catalog["books"])


def authorSize(catalog):
    return lt.size(catalog["authors"])


def tagSize(catalog):
    return lt.size(catalog["tags"])


def bookTagSize(catalog):
    return lt.size(catalog["book_tags"])


# Funciones utilizadas para comparar elementos dentro de una lista

def compareauthors(authorname1, author):
    if authorname1.lower() == author["name"].lower():
        return 0
    elif authorname1.lower() > author["name"].lower():
        return 1
    return -1


def comparetagnames(name, tag):
    if (name == tag["name"]):
        return 0
    elif (name > tag["name"]):
        return 1
    return -1


def comparebooks(bookid1, book):
    if bookid1 == book["goodreads_book_id"]:
        return 0
    elif bookid1 > book["goodreads_book_id"]:
        return 1
    return -1


# funciones para comparar elementos dentro de algoritmos de ordenamientos

def compareISBN(book1, book2):
    """
    compara dos libros por su ISBN
    """
    # TODO examinar el criterio de ordenamiento (parte 1)
    return (str(book1["isbn13"]) > str(book2["isbn13"]))


# Funciones de ordenamiento

def sortBooks(catalog):
    """
    Ordena los libros por ISBN
    """
    # TODO examinar el ordenamiento (parte 1)
    # toma la lista de libros del catalogo
    books = catalog["books"]
    # ordena la lista de libros
    sorted_list = qs.sort(books, compareISBN)
    # actualiza la lista de libros del catalogo
    catalog["books"] = sorted_list
    return sorted_list


def shuffleBooks(catalog):
    """
    Desordena los libros dentro del catalogo
    """
    # TODO examinar la funcion para desordenar (parte 1)
    books = catalog["books"]
    element_num = lt.size(books)
    # creo la nueva lista desordenada vacia
    shuffled_list = lt.newList("ARRAY_LIST",
                               cmpfunction=comparebooks)
    i = 0
    # itero la lista de libros y agrego un libro aleatorio a la nueva lista
    while i < element_num:
        # reviso el numero de libros
        tsize = lt.size(books)
        # selecciono un indice aleatorio de un libro
        ridx = random.randint(1, tsize)
        # agregro el libro a la nueva lista y lo elimino de la lista original
        lt.addLast(shuffled_list, lt.getElement(books, ridx))
        lt.deleteElement(books, ridx)
        i += 1
    # actualizo la lista de libros del catalogo
    catalog["books"] = shuffled_list
    return shuffled_list


# Funciones de busqueda y filtros

def searchBookByISBN(catalog, bookisbn):
    """searchBookByISBN es la MASCARA para la busqueda recursiva, recibe el
    catalogo y el ISBN del libro buscarlo en la lista de libros del catalogo
    y prepara las condiciones para la recursion

    Args:
        catalog (dict): el catalogo de libros
        bookisbn (int): el ISBN del libro que se busca

    Returns:
        book: el diccionario que cumple con el ISBN dentro de la
        lista de libros
    """
    books=catalog["books"]
    bajo = 1
    tamaño = lt.size(books)
    # TODO implementar la mascara de la busqueda recursiva (parte 2)
    buscarISBN = recursiveSearchBookByISBN(books, bookisbn, bajo, tamaño)
    if buscarISBN == -1:
        return None
    else:
        return lt.getElement(books, buscarISBN)


def recursiveSearchBookByISBN(books, bookisbn, low, high):
    """recursiveSearchBookByISBN ejecuta recursivamente la busqueda binaria
    el ISBN del libro en la lista, si no lo encuentra retorna -1, utiliza la
    llave "isbn13" para la comparacion

    Args:
        books (ADT List): lista de libros en el catalogo
        bookisbn (int): ISBN del libro que se busca
        low (int): rango inferior de busqueda
        high (int): rango superior de busqueda

    Returns:
        int: indice del libro en la lista, -1 si no lo encuentra
    """
    # TODO implementar recursivamente binary search (parte 2)
    if high >= low:
        intermedio = (high+low)//2
        if compareISBN({"isbn13":bookisbn}, lt.getElement(books, intermedio)):
            return recursiveSearchBookByISBN(books, bookisbn, low, intermedio-1)
        elif lt.getElement(books, intermedio)["isbn13"] == bookisbn:
            return intermedio
        else:
            return recursiveSearchBookByISBN(books, bookisbn, intermedio+1, high)
    else:
        return -1    
        

def iterativeSearchBookByISBN(catalog, bookid):
    """iterativeSearchBookByISBN ejecuta iterativamente la busqueda binaria el
    ISBN del libro en la lista, si no lo encuentra retorna -1, utiliza la llave
    "isbn13" para la comparacion

    Args:
        catalog (dict): el catalogo de libros
        bookisbn (int): ISBN del libro que se busca

    Returns:
        book: el diccionario que cumple con el ISBN dentro de la
        lista de libros
    """
    # TODO implementar iterativamente del binary search (parte 2)
    books = catalog["books"]
    bajo = 1
    tamaño = lt.size(books)
    mitad = 0
    book = {"isbn13": bookid}
    while bajo <= tamaño:
        mitad = (tamaño+bajo)//2
        if compareISBN(lt.getElement(books, mitad), book):
            bajo = mitad-1
        elif compareISBN(book, lt.getElement(books, mitad)):
            tamaño = mitad+1
        else:
            return lt.getElement(books, mitad)
    return None



# funciones para calcular estadisticas

def AvgBooksRatings(catalog):
    """AvgBooksRatings es la MASCARA para el calculo recursivo del promedio de
    ratings de los libros en el catalogo, utiliza la llave "average_rating" y
    prepara las condiciones para la recursion

    Args:
        catalog (dict): el catalogo de libros

    Returns:
        float: promedio de ratings de los libros en el catalogo
    """
    def recursiveAvgBooksRating(books, idx, n):
        """recursiveAvgBooksRating ejecuta recursivamente el promedio de ratings
        teniendo en cuenta el indice de inicio y el total de libros a procesar por
        la llave "average_rating"

        Args:
            books (ADT List): lista de libros en el catalogo
            idx (int): indice de inicio de la lista
            n (int): total de libros a procesar

        Returns:
            float: promedio de ratings de los libros en la lista
        """
        if n == 0:
            return 0.0
        rating = books[idx]["average_rating"]
        if n == 1:
            return rating
        restos = recursiveFilterBooksByRating(books, idx+1, n-1)
        return (rating + restos * (n-1))/n
    books = list(catalog.values())
    recursive = recursiveAvgBooksRating(books, 0, len(books))
    return recursive


def iterativeAvgBooksRating(catalog):
    """iterativeAvgBooksRating calcula iterativamente el promedio de ratings de
    los libros en el catalogo, utiliza la llave "average_rating" y devuelve el
    promedio de todos los libros

    Args:
        catalog (dict): el catalogo de libros

    Returns:
        float: promedio de ratings de los libros en la lista
    """
    total_rating = 0
    cantidad_libros = 0
    rating = 0.0
    for i in catalog.values():
        if "average_rating" in i:
            total_rating += i["avarage_rating"]
            cantidad_libros += 1
    if cantidad_libros == 0:
        return 0.0
    rating = total_rating / cantidad_libros
    return rating


def filterBooksByRating(catalog, low, high):
    """filteringBooksByRating es la MASCARA para el filtrado recursivo de
    libros por rating, utiliza la llave "average_rating" y devuelve una lista
    de libros, tambien prepara las condiciones para la recursion

    Args:
        catalog (dict): el catalogo de libros
        low (float): limite inferior de busqueda para el rating
        high (float): limite superior de busqueda para el rating

    Returns:
        ADT List: listado de libros que cumplen con el rango de rating
    """
    # TODO implementar la mascara recursiva para filtrar libros (parte 2)
    pass


def recursiveFilterBooksByRating(books, answer, low, high, idx=1):
    """recursiveFilterBooksByRating filtra recursivamente los libros por
    rating, utiliza la llave "average_rating" y devuelve una lista de libros
    que se pasan inicialmente vacia por parametro y por defecto inicia el
    recorrido por el primer elemento de la lista

    Args:
        books (ADT List): lista de libros en el catalogo
        answer (ADT List): lista de libros filtrados, inicialmente vacia
        low (_type_): limite inferior de busqueda para el rating
        high (_type_): limite superior de busqueda para el rating
        idx (int, optional): indice de inicio de la lista. por defecto 1.
    Returns:
        ADT List: lista de libros filtrados
    """
    # TODO implementar recursivamente el filtrado de libros (parte 2)
    pass


def iterativeFilterBooksByRating(catalog, low, high):
    """iterativeFilterBooksByRating filtra iterativamente los libros por
    rating, utiliza la llave "average_rating" y devuelve una lista de libros
    si ninguno cumple con el rango de rating, devuelve una lista vacia

    Args:
        catalog (dict): el catalogo de libros
        low (_type_): limite inferior de busqueda para el rating
        high (_type_): limite superior de busqueda para el rating

    Returns:
        ADT List: lista de libros filtrados, inicialmente vacia y por
        defecto SINGLE_LINKED
    """
    # TODO implementar iterativamente el filtrado de libros (parte 2)
    pass
