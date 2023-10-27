FROM nginx:1.24-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN sed -i 's/.*server_names_hash_bucket_size.*/\t server_names_hash_bucket_size 64;/' /etc/nginx/nginx.conf

