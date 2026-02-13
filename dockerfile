FROM wordpress:5.7

COPY config/plugins/wpdiscuz /var/www/html/wp-content/plugins/wpdiscuz

RUN chown -R www-data:www-data /var/www/html/wp-content/plugins/wpdiscuz
