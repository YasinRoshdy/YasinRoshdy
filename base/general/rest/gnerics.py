# from rest_framework.generics import ListAPIView


# class ListApiByInput(ListAPIView):

#     serializer_class = None
#     queryset = None

#     # should be typle of typle
#     # ex:
#     # (("sura_id", "int"),('hadith_id','int'))
#     fields = (("sura_id", "int"), ("hadith_id", "int"))
#     # default is or
#     # 'or' | 'and'
#     condition = "or"

#     def get(self, request):

#         # try:
#         if not self.fields:
#             raise Exception('sould impelement fields as typle of typles(("sura_id", "int"),("hadith_id","int"))')
#         for el in self.fields:
#             item = el[0]
#             _type = el[1]

#             book_id = _type(request.query_params.get(item))
#             if not (book_id and isinstance(book_id, _type)):
#                 raise Exception(f"ListApiByInput : item and isinstance({item}, {_type})", book_id, _type(book_id))

#         self.get_queryset().filter()
#     # except Exception:

#     #     return ResponseRest(
#     #         {"success": False, "message": api_message_should_send_parameter("book_id:<int>")},
#     #         status=HTTP_400_BAD_REQUEST,
#     #     )
