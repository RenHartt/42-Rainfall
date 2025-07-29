#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define	STACK_ADDR_HINT	0xb0000000

char	*p(void)
{
	void	*pad;
	void	*pad2;
	void	*addr;
	char	buffer[64];

	fflush(stdout);
	
	gets(buffer);
	addr = &pad2 + 2;
	if (((unsigned int)addr & STACK_ADDR_HINT) == STACK_ADDR_HINT)
	{
		printf("(%p)\n", addr);
		exit(1);
	}
	puts(buffer);
	return (strdup(buffer));
}

int main(void)
{
	p();
}
