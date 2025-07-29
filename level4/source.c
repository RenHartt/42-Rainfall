#include <stdio.h>
#include <stdlib.h>

#define CHECK	0x01025544

int m = 0;

void	p(char *buffer)
{
	printf(buffer);
}

void	n(void)
{
	char	buffer[512];

	fgets(buffer, sizeof(buffer), stdin);
	p(buffer);
	if (m == CHECK)
		system("/bin/sh");
}

int main(void)
{
	n();
}
