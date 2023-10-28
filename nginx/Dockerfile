FROM nginx:1.24-alpine

# remove default config from nginx
RUN if [ -f "/etc/nginx/conf.d/default.conf" ]; then \
    echo "nginx.conf exists, removing ... " && \
    rm "/etc/nginx/conf.d/default.conf"; \
fi

RUN if [ -f "/etc/nginx/conf.d/nginx.conf" ]; then \
    echo "nginx.conf exists, removing ... " && \
    rm "/etc/nginx/conf.d/nginx.conf"; \
fi

RUN if [ -f "/etc/nginx/conf.d/nginx.dev.conf" ]; then \
    echo "nginx.dev.conf exists, removing ... " && \
    rm "/etc/nginx/conf.d/nginx.dev.conf"; \
fi

COPY nginx.conf /etc/nginx/conf.d

RUN sed -i 's/.*server_names_hash_bucket_size.*/\t server_names_hash_bucket_size 64;/' /etc/nginx/nginx.conf

