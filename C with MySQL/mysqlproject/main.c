#define _CRT_SECURE_NO_WARNINGS
#include <mysql.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <csv.h>

// MySQL 연결 정보
const char* host = "ssu-info.civydey9zqjl.us-east-2.rds.amazonaws.com";
const char* user = "admin";
const char* password = "reapinjoy"; // 실제 코드에서는 안전한 방법으로 관리해야 함
const char* database = "ssu_info";
unsigned int port = 3306;
const char* unix_socket = NULL;
unsigned long client_flag = 0;

// MySQL 에러 처리
void finish_with_error(MYSQL* con) {
    fprintf(stderr, "MySQL error: %s\n", mysql_error(con));
    mysql_close(con);
    exit(1);
}

// 카테고리 ID 가져오기(비교용)
int get_category_id(MYSQL* con, const char* univ_name, const char* dep_name) {
    int category_id = -1;
    char query[1024];

    // 쿼리 생성
    snprintf(query, sizeof(query), "SELECT id FROM categories WHERE univ_name = '%s' AND dep_name = '%s'", univ_name, dep_name);

    //쿼리 실행
    if (mysql_query(con, query)) {
        finish_with_error(con); //오류 처리 함수 호출
    }

    // 결과 집합 가져오기
    MYSQL_RES* result = mysql_store_result(con);

    if (result == NULL) {
        finish_with_error(con); //오류 처리 함수 호출
    }

    // 결과에서 첫 번째 행 가져오기
    MYSQL_ROW row = mysql_fetch_row(result);

    if (row && row[0]) {
        category_id = atoi(row[0]);
    } // 문자열을 정수로 변환

    mysql_free_result(result); // 결과 집합 메모리 해제
    return category_id;
}

// 카테고리2 ID를 가져오는 함수 (음식, 건강 등 제휴사업 정보를 분류한 카테고리)
int get_category2_id(MYSQL* con, const char* category2_name) {
    int category2_id = -1;
    char query[1024];

    // 쿼리 생성
    snprintf(query, sizeof(query), "SELECT id FROM aff_categories WHERE name = '%s'", category2_name);

    //쿼리 실행
    if (mysql_query(con, query)) {
        finish_with_error(con); //오류 처리 함수 호출
    }

    // 결과 집합 가져오기
    MYSQL_RES* result = mysql_store_result(con);

    if (result == NULL) {
        finish_with_error(con); //오류 처리 함수 호출
    }

    // 결과에서 첫 번째 행 가져오기
    MYSQL_ROW row = mysql_fetch_row(result);

    if (row && row[0]) {
        category2_id = atoi(row[0]);
    } // 문자열을 정수로 변환

    mysql_free_result(result); // 결과 집합 메모리 해제
    return category2_id;
}

int main() {
    // MySQL 연결 초기화
    MYSQL* con = mysql_init(NULL);
    if (con == NULL) {
        fprintf(stderr, "mysql_init() failed\n");
        exit(1);
    }

    // MySQL 데이터베이스에 연결
    if (mysql_real_connect(con, host, user, password, database, port, unix_socket, client_flag) == NULL) {
        finish_with_error(con);
    }

    // CSV 파일 열기
    FILE* file = fopen("aff_infos.csv", "r");
    if (file == NULL) {
        perror("Error opening file");
        exit(1);
    }

    // libcsv 라이브러리 초기화
    csv_parser parser;
    if (csv_init(&parser, 0) != 0) {
        perror("csv_init() failed");
        exit(1);
    }

    char line[1024];
    char* univ_name, * dep_name, * description, * start_date, * end_date, * category2_name;

    while (fgets(line, sizeof(line), file)) {
        // CSV 파일 파싱
        if (csv_parse(&parser, line, strlen(line), &univ_name, &dep_name, NULL, &description, &start_date, &end_date, &category2_name) != 6) {
            fprintf(stderr, "Parsing error\n");
            continue;
        }

        int category_id = get_category_id(con, univ_name, dep_name);
        int category2_id = get_category2_id(con, category2_name);

        if (category_id == -1 || category2_id == -1) {
            fprintf(stderr, "Invalid category ID found\n");
            continue;
        }

        // 쿼리 생성
        char query[1024];
        snprintf(query, sizeof(query), "INSERT INTO aff_info (categories_id, description, start_date, end_date, categories2_id) VALUES (%d, '%s', '%s', '%s', %d)",
            category_id, description, start_date, end_date, category2_id);

        if (mysql_query(con, query)) {
            finish_with_error(con);
        }
    }

    // libcsv 라이브러리를 해제합니다.
    csv_fini(&parser, NULL, NULL, NULL);
    fclose(file);
    mysql_close(con);
    return 0;
}